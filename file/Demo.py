import subprocess
import os
import sys
import ctypes
import time
from datetime import datetime


def is_admin():
    """Check if the script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def get_disk_number(drive_letter):
    """Get the physical disk number for a given drive letter."""
    try:
        cmd = f"wmic logicaldisk where DeviceID='{drive_letter}:' get DeviceID,DriveType"
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if "2" in result.stdout:  # DriveType 2 = Removable
            cmd = f"wmic volume where DriveLetter='{drive_letter}:' get DiskNumber"
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            return result.stdout.split()[-1]
        return None
    except subprocess.CalledProcessError:
        return None


def repair_usb(drive_letter, filesystem='FAT32', drive_label='USB_DRIVE', quick_format=True, force_clean=False):
    """
    Repair and format a USB drive.
    """
    try:
        # Validation
        if not is_admin():
            raise PermissionError("This tool requires Administrator privileges")

        if len(drive_letter) != 1 or not drive_letter.isalpha():
            raise ValueError("Invalid drive letter")

        fs = filesystem.upper()
        if fs not in ('FAT32', 'NTFS', 'EXFAT'):
            raise ValueError("Invalid filesystem. Use FAT32, NTFS, or exFAT")

        disk_number = get_disk_number(drive_letter)
        if not disk_number:
            raise ValueError("Drive not found or not removable")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"usb_repair_log_{timestamp}.txt"

        # Step 1: DiskPart operations
        diskpart_script = f"""
        list disk
        select disk {disk_number}
        detail disk
        {"attributes disk clear readonly" if not force_clean else "clean"}
        clean
        create partition primary
        format fs={fs} {"quick" if quick_format else ""} label="{drive_label}"
        assign letter={drive_letter}
        exit
        """

        with open("diskpart_script.txt", "w") as f:
            f.write(diskpart_script.strip())

        # Execute with logging
        with open(log_file, "a") as log:
            log.write(f"=== DiskPart Operations ===\n")
            subprocess.run(f"diskpart /s diskpart_script.txt", shell=True, check=True, stdout=log, stderr=log)

        # Step 2: Filesystem check
        with open(log_file, "a") as log:
            log.write(f"\n=== CHKDSK Operations ===\n")
            subprocess.run(f"chkdsk {drive_letter}: /f /r /x", shell=True, check=True, stdout=log, stderr=log)

        # Step 3: Verify repair
        verify_cmd = f"fsutil fsinfo volumeinfo {drive_letter}:"
        result = subprocess.run(verify_cmd, shell=True, check=True, capture_output=True, text=True)

        print(f"\n[SUCCESS] Drive {drive_letter}:")
        print(f"• Formatted as {fs} with label '{drive_label}'")
        print(f"• Details:\n{result.stdout}")
        print(f"• Log saved to {log_file}")

        # Cleanup
        os.remove("diskpart_script.txt")
        return True

    except subprocess.CalledProcessError as e:
        error_msg = f"Command failed: {e.stderr if e.stderr else e}"
        with open(log_file, "a") as log:
            log.write(f"\n[ERROR] {error_msg}")
        print(f"\n[ERROR] {error_msg}\nSee {log_file} for details")
        return False
    except Exception as e:
        print(f"\n[FATAL ERROR] {str(e)}")
        return False


def main():
    print("=== Advanced USB Drive Repair Tool ===")
    print("Note: Requires Administrator privileges\n")

    if not is_admin():
        print("Please restart this program as Administrator!")
        time.sleep(5)
        sys.exit(1)

    # User inputs with validation
    while True:
        drive_letter = input("Enter drive letter (e.g., E): ").strip().upper()
        if len(drive_letter) == 1 and drive_letter.isalpha():
            break
        print("Invalid input. Enter a single letter (A-Z)")

    filesystem = input("Filesystem [FAT32/NTFS/exFAT] (default FAT32): ").strip().upper() or 'FAT32'
    drive_label = input("Drive label (optional): ").strip() or 'USB_DRIVE'
    quick_format = input("Quick format? [Y/n]: ").strip().upper() != 'N'
    force_clean = input("Force clean (for stubborn drives)? [y/N]: ").strip().upper() == 'Y'

    print("\nStarting repair process...")
    success = repair_usb(
        drive_letter=drive_letter,
        filesystem=filesystem,
        drive_label=drive_label,
        quick_format=quick_format,
        force_clean=force_clean
    )

    if success:
        print("\nRepair completed successfully!")
    else:
        print("\nRepair failed. See error messages above.")

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
