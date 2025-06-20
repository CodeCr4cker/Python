import PyPDF2
import zipfile
import rarfile
import os

def dictionary_attack(file_path, password_list_path):
    # Determine the file type
    file_ext = os.path.splitext(file_path)[1].lower()

    # Read the password list
    with open(password_list_path, 'r', encoding='utf-8', errors='ignore') as file:
        passwords = [line.strip() for line in file]

    # Try passwords based on file type
    if file_ext == '.pdf':
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for password in passwords:
                if pdf_reader.decrypt(password):
                    print(f"[+] Password found: {password}")
                    return password
    elif file_ext == '.zip':
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            for password in passwords:
                try:
                    zip_file.extractall(pwd=password.encode())
                    print(f"[+] Password found: {password}")
                    return password
                except (RuntimeError, zipfile.BadZipFile):
                    continue
    elif file_ext == '.rar':
        with rarfile.RarFile(file_path, 'r') as rar_file:
            for password in passwords:
                try:
                    rar_file.extractall(pwd=password)
                    print(f"[+] Password found: {password}")
                    return password
                except (rarfile.BadRarFile, rarfile.PasswordRequired):
                    continue
    else:
        print("[-] Unsupported file format. Please use PDF, ZIP, or RAR.")
        return None

    print("[-] Password not found in the list.")
    return None

# Example usage
if __name__ == "__main__":
    file_path = input("Enter the path to the locked file (PDF/ZIP/RAR): ")
    password_list_path = input("Enter the path to the password list (TXT): ")
    dictionary_attack(file_path, password_list_path)
