# Import required libraries
import PyPDF2
import os
import sys
from tqdm import tqdm  # For progress bar
from colorama import Fore, init  # For colored output
import pyfiglet  # For ASCII art banner

# Initialize colorama for cross-platform colored output
init(autoreset=True)

def display_banner():
    """Display a festive banner using pyfiglet."""
    banner = pyfiglet.figlet_format('Eid Mubarak', font='slant')
    print(Fore.GREEN + banner)
    print(Fore.CYAN + "PDF Dictionary Attack Tool")
    print(Fore.CYAN + "=" * 30 + "\n")

def pdf_dictionary_attack(pdf_path, password_list_path):
    """
    Perform a dictionary attack on a locked PDF file.

    Args:
        pdf_path (str): Path to the locked PDF file.
        password_list_path (str): Path to the password list (TXT file).

    Returns:
        str: The found password, or None if not found.
    """
    # Validate file paths
    if not os.path.isfile(pdf_path):
        print(Fore.RED + f"[-] Error: PDF file not found at {pdf_path}")
        return None
    if not os.path.isfile(password_list_path):
        print(Fore.RED + f"[-] Error: Password list file not found at {password_list_path}")
        return None

    try:
        # Open the PDF file
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Check if PDF is encrypted
            if not pdf_reader.is_encrypted:
                print(Fore.YELLOW + "[-] The PDF file is not encrypted.")
                return None

            # Read password list
            with open(password_list_path, 'r', encoding='utf-8', errors='ignore') as file:
                passwords = [line.strip() for line in file if line.strip()]

            # Check if password list is empty
            if not passwords:
                print(Fore.RED + "[-] Error: Password list is empty.")
                return None

            print(Fore.BLUE + f"[*] Total passwords to try: {len(passwords)}")
            print(Fore.BLUE + "[*] Starting dictionary attack...\n")

            # Initialize progress bar
            progress_bar = tqdm(
                passwords,
                desc=Fore.MAGENTA + "Progress",
                unit="password",
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}"
            )

            # Try each password
            for password in progress_bar:
                if pdf_reader.decrypt(password):
                    progress_bar.close()
                    print(Fore.GREEN + f"\n[+] Password found: {password}")
                    return password

            # If no password worked
            progress_bar.close()
            print(Fore.RED + "\n[-] Password not found in the list.")
            return None

    except Exception as e:
        print(Fore.RED + f"[-] Error: {str(e)}")
        return None

if __name__ == "__main__":
    # Display festive banner
    display_banner()

    # Prompt user for file paths
    pdf_path = input(Fore.WHITE + "[?] Enter the path to the locked PDF file: ")
    password_list_path = input(Fore.WHITE + "[?] Enter the path to the password list (TXT): ")

    # Perform the attack
    found_password = pdf_dictionary_attack(pdf_path, password_list_path)

    # Exit message
    if found_password:
        print(Fore.GREEN + "\n[+] Success! Exiting...")
    else:
        print(Fore.RED + "\n[-] Failed to unlock the PDF. Exiting...")
