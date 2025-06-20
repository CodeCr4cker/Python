# Import the PyPDF2 library to handle PDF operations like reading and decrypting
import PyPDF2

def pdf_dictionary_attack(pdf_path, password_list_path):
    """
    Perform a dictionary attack on a locked PDF file.

    Args:
        pdf_path (str): Path to the locked PDF file.
        password_list_path (str): Path to the password list (TXT file).
    """

    # Open the PDF file in binary read mode ('rb') to ensure proper handling of the file
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PdfReader object to interact with the PDF file
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Check if the PDF is encrypted by calling the is_encrypted property
        if not pdf_reader.is_encrypted:
            # If the PDF is not encrypted, inform the user and exit the function
            print("[-] The PDF file is not encrypted.")
            return None

        # Open the password list file in read mode with UTF-8 encoding
        # 'errors='ignore'' skips any problematic characters in the file
        with open(password_list_path, 'r', encoding='utf-8', errors='ignore') as file:
            # Read all lines from the file, strip whitespace, and store them in a list
            passwords = [line.strip() for line in file]

        # Iterate over each password in the passwords list
        for password in passwords:
            # Attempt to decrypt the PDF using the current password
            # The decrypt() method returns True if the password is correct
            if pdf_reader.decrypt(password):
                # If the password is correct, print it and return it
                print(f"[+] Password found: {password}")
                return password

        # If no password in the list worked, inform the user
        print("[-] Password not found in the list.")
        return None

# Entry point of the script
if __name__ == "__main__":
    # Prompt the user to enter the path to the locked PDF file
    pdf_path = input("Enter the path to the locked PDF file: ")
    
    # Prompt the user to enter the path to the password list (TXT file)
    password_list_path = input("Enter the path to the password list (TXT): ")
    
    # Call the function to perform the dictionary attack
    pdf_dictionary_attack(pdf_path, password_list_path)
