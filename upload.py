import mysql.connector
from tkinter import Tk, filedialog, Listbox, Button, messagebox

# Step 1: Connect to the MySQL database
connection = mysql.connector.connect (
    host="localhost",
    user="root",
    port=330,
    password="Hacker@85",
    database="upload"
)
cursor = connection.cursor()

# Step 2: Create the table (if not already exists)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INT AUTO_INCREMENT PRIMARY KEY,
        file_name VARCHAR(255) NOT NULL,
        file_type VARCHAR(50) NOT NULL,
        file_data LONGBLOB NOT NULL
    )
''')
connection.commit()

# Step 3: Function to insert a file
def insert_file(file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
    file_name = file_path.split('/')[-1]
    file_type = file_name.split('.')[-1].lower()  # Extract file extension
    cursor.execute('''
        INSERT INTO files (file_name, file_type, file_data) VALUES (%s, %s, %s)
    ''', (file_name, file_type, file_data))
    connection.commit()
    print(f"'{file_name}' uploaded successfully.")
    messagebox.showinfo("Success", f"'{file_name}' uploaded successfully.")

# Step 4: Function to display uploaded files
def display_files():
    cursor.execute('SELECT id, file_name, file_type FROM files')
    files = cursor.fetchall()
    file_listbox.delete(0, 'end')  # Clear the listbox
    for file in files:
        file_listbox.insert('end', f"{file[0]}: {file[1]} ({file[2]})")  # Show ID, name, and type

# Step 5: Function to download a file
def download_file():
    selected = file_listbox.get(file_listbox.curselection())
    if selected:
        file_id = selected.split(":")[0]
        cursor.execute('SELECT file_name, file_data FROM files WHERE id = %s', (file_id,))
        file_data = cursor.fetchone()
        if file_data:
            save_path = filedialog.asksaveasfilename(
                title="Save File As",
                initialfile=file_data[0],
                defaultextension=".*",
                filetypes=[("All Files", "*.*"), ("PDF Files", "*.pdf"), ("Images", "*.jpg;*.png;*.jpeg")]
            )
            if save_path:
                with open(save_path, 'wb') as file:
                    file.write(file_data[1])
                messagebox.showinfo("Success", f"File saved as {save_path}.")
        else:
            messagebox.showerror("Error", "File not found in the database.")
    else:
        messagebox.showerror("Error", "Please select a file to download.")

# Step 6: Function to select and upload a file
def select_file_and_upload():
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[
            ("All Supported Files", "*.pdf;*.jpg;*.png;*.jpeg"),
            ("PDF Files", "*.pdf"),
            ("Image Files", "*.jpg;*.png;*.jpeg")
        ]
    )
    if file_path:
        insert_file(file_path)
        display_files()
    else:
        print("No file selected.")

# Step 7: Create the GUI
root = Tk()
root.title("File Manager")

# Listbox to display files
file_listbox = Listbox(root, width=60, height=20)
file_listbox.pack(pady=10)

# Buttons for upload and download
upload_button = Button(root, text="Upload File", command=select_file_and_upload)
upload_button.pack(pady=5)

download_button = Button(root, text="Download Selected File", command=download_file)
download_button.pack(pady=5)

# Populate the listbox with existing files
display_files()

# Run the application
root.mainloop()

# Step 8: Close the connection on exit
cursor.close()
connection.close()