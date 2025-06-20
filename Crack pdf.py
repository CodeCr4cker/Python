import PyPDF2

def pdf_dictionary_attack(pdf_path, password_list_path):
    """
    Perform a dictionary attack on a locked PDF file.

    Args:
        pdf_path (str): Path to the locked PDF file.
        password_list_path (str): Path to the password list (TXT file).
    """
    # Open the PDF file in binary mode
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Check if the PDF is encrypted
        if not pdf_reader.is_encrypted:
            print("[-] The PDF file is not encrypted.")
            return None

        # Read the password list
        with open(password_list_path, 'r', encoding='utf-8', errors='ignore') as file:
            passwords = [line.strip() for line in file]

        # Try each password in the list
        for password in passwords:
            if pdf_reader.decrypt(password):
                print(f"[+] Password found: {password}")
                return password

        # If no password worked
        print("[-] Password not found in the list.")
        return None

# Example usage
if __name__ == "__main__":
    pdf_path = input("Enter the path to the locked PDF file: ")
    password_list_path = input("Enter the path to the password list (TXT): ")
    pdf_dictionary_attack(pdf_path, password_list_path)
  
