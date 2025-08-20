import mysql.connector
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import io

# ----------------- CONNECT TO DATABASE -----------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",        # your MySQL host
        user="root",             # your MySQL username
        password="password",     # your MySQL password
        database="testdb"        # your database
    )

# ----------------- CREATE TABLE -----------------
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            grade VARCHAR(10),
            photo LONGBLOB
        )
    """)
    conn.commit()
    conn.close()

# ----------------- CRUD + PHOTO -----------------
def insert_student(name, age, grade, filepath=None):
    conn = get_connection()
    cursor = conn.cursor()
    binary_data = None
    if filepath:
        with open(filepath, "rb") as file:
            binary_data = file.read()
    query = "INSERT INTO students (name, age, grade, photo) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, age, grade, binary_data))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student added successfully!")

def search_student(name):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT id, name, age, grade FROM students WHERE name = %s"
    cursor.execute(query, (name,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_student(student_id, new_name, new_age, new_grade):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE students SET name=%s, age=%s, grade=%s WHERE id=%s"
    cursor.execute(query, (new_name, new_age, new_grade, student_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student updated successfully!")

def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM students WHERE id=%s"
    cursor.execute(query, (student_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student deleted successfully!")

def get_photo(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT photo FROM students WHERE id=%s"
    cursor.execute(query, (student_id,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0]:
        return result[0]
    return None

# ----------------- GUI FUNCTIONS -----------------
selected_file = None

def choose_photo():
    global selected_file
    selected_file = filedialog.askopenfilename(
        title="Choose Profile Photo",
        filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
    )
    if selected_file:
        messagebox.showinfo("Selected", f"Photo selected:\n{selected_file}")

def add_student_gui():
    insert_student(entry_name.get(), entry_age.get(), entry_grade.get(), selected_file)

def search_student_gui():
    result = search_student(entry_name.get())
    text_area.delete("1.0", END)
    if result:
        for row in result:
            text_area.insert(END, f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Grade: {row[3]}\n")
    else:
        text_area.insert(END, "No student found.\n")

def update_student_gui():
    try:
        update_student(int(entry_id.get()), entry_name.get(), entry_age.get(), entry_grade.get())
    except:
        messagebox.showerror("Error", "Enter valid ID!")

def delete_student_gui():
    try:
        delete_student(int(entry_id.get()))
    except:
        messagebox.showerror("Error", "Enter valid ID!")

def show_photo_gui():
    try:
        binary_data = get_photo(int(entry_id.get()))
        if binary_data:
            image = Image.open(io.BytesIO(binary_data))
            image = image.resize((150, 150))
            img = ImageTk.PhotoImage(image)
            label_photo.config(image=img)
            label_photo.image = img
        else:
            messagebox.showerror("Error", "No photo found for this student.")
    except:
        messagebox.showerror("Error", "Enter valid ID!")

# ----------------- MAIN GUI -----------------
root = Tk()
root.title("Student Manager with Photos")
root.geometry("600x600")

create_table()

# Entry fields
Label(root, text="ID (for update/delete/show):").pack()
entry_id = Entry(root)
entry_id.pack()

Label(root, text="Name:").pack()
entry_name = Entry(root)
entry_name.pack()

Label(root, text="Age:").pack()
entry_age = Entry(root)
entry_age.pack()

Label(root, text="Grade:").pack()
entry_grade = Entry(root)
entry_grade.pack()

# Buttons with jade green style
Button(root, text="Choose Photo", bg="#00a86b", fg="white", command=choose_photo).pack(pady=5)
Button(root, text="Add Student", bg="#00a86b", fg="white", command=add_student_gui).pack(pady=5)
Button(root, text="Search Student", bg="#00a86b", fg="white", command=search_student_gui).pack(pady=5)
Button(root, text="Update Student", bg="#00a86b", fg="white", command=update_student_gui).pack(pady=5)
Button(root, text="Delete Student", bg="#00a86b", fg="white", command=delete_student_gui).pack(pady=5)
Button(root, text="Show Photo", bg="#00a86b", fg="white", command=show_photo_gui).pack(pady=5)

# Text area for results
text_area = Text(root, height=8, width=60)
text_area.pack(pady=10)

# Label for showing photo
label_photo = Label(root)
label_photo.pack(pady=20)

root.mainloop()
connection.close()
