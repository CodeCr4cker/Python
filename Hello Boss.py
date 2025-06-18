import os
import shutil
import speech_recognition as sr
import pyttsx3
import webbrowser
import time
import subprocess
from tkinter import Tk, Label, Button, Text, Scrollbar, END
import json
from datetime import datetime
from ics import Calendar, Event
import pyautogui  # For volume control (Windows)
from getpass import getpass
import hashlib

# Initialize TTS engine
engine = pyttsx3.init()

# Security: Password hash (for demo, use proper encryption in production)
PASSWORD_HASH = hashlib.sha256(b"admin123").hexdigest()

# Log file
LOG_FILE = "assistant_log.txt"

# Supported languages (for speech recognition)
SUPPORTED_LANGUAGES = {
    "english": "en-US",
    "spanish": "es-ES",
    "french": "fr-FR",
}

# Initialize GUI
class AssistantGUI:
    def __init__(self, master):
        self.master = master
        master.title("Voice Assistant Dashboard")
        self.status_label = Label(master, text="Status: Ready", fg="green")
        self.status_label.pack()
        self.log_text = Text(master, height=10, width=50)
        self.log_text.pack()
        self.scrollbar = Scrollbar(master, command=self.log_text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=self.scrollbar.set)

    def update_log(self, message):
        self.log_text.insert(END, f"{datetime.now()}: {message}\n")
        self.log_text.see(END)

    def update_status(self, status, color="green"):
        self.status_label.config(text=f"Status: {status}", fg=color)

# Initialize GUI
root = Tk()
gui = AssistantGUI(root)
root.update()

def speak(text):
    """Convert text to speech and update GUI."""
    gui.update_log(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen(language="en-US"):
    """Listen to user's voice command."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        gui.update_status("Listening...", "blue")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio, language=language).lower()
        gui.update_log(f"User: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please try again.")
        return ""
    except sr.RequestError:
        speak("Sorry, my speech service is down. Please try again later.")
        return ""

def authenticate():
    """Voice or password authentication."""
    speak("Please say the passphrase or enter the password.")
    auth_method = listen()
    if auth_method and "Hello Boss" in auth_method:
        return True
    else:
        password = getpass("Enter password: ")
        if hashlib.sha256(password.encode()).hexdigest() == PASSWORD_HASH:
            return True
    speak("Authentication failed.")
    return False

def create_folder(folder_name):
    """Create a new folder."""
    try:
        os.mkdir(folder_name)
        speak(f"Folder {folder_name} created successfully.")
    except FileExistsError:
        speak(f"Folder {folder_name} already exists.")

def list_files(folder_path):
    """List files in a directory."""
    if os.path.exists(folder_path):
        files = os.listdir(folder_path)
        speak(f"Files in {folder_path}: {', '.join(files)}")
    else:
        speak("Folder does not exist.")

def rename_file(old_name, new_name):
    """Rename a file or folder."""
    if os.path.exists(old_name):
        os.rename(old_name, new_name)
        speak(f"Renamed {old_name} to {new_name}.")
    else:
        speak("File or folder not found.")

def copy_file(source, destination):
    """Copy a file to a destination."""
    if os.path.exists(source):
        shutil.copy(source, destination)
        speak(f"Copied {source} to {destination}.")
    else:
        speak("Source file not found.")

def open_app(app_name):
    """Open an application."""
    apps = {
        "chrome": "open chrome",
        "notepad": "open notepad",
        "calculator": "open calculator",
        "WhatsApp":"open WhatsApp",
        "camera":"open camera",
        
    }
    if app_name in apps:
        os.system(apps[app_name])
        speak(f"Opening {app_name}.")
    else:
        speak("Application not supported.")

def set_reminder(reminder_text, reminder_time):
    """Set a reminder."""
    with open("reminders.txt", "a") as f:
        f.write(f"{reminder_time}: {reminder_text}\n")
    speak(f"Reminder set for {reminder_time}.")

def adjust_volume(action):
    """Adjust system volume (Windows only)."""
    if action == "increase":
        pyautogui.press("volumeup")
    elif action == "decrease":
        pyautogui.press("volumedown")
    elif action == "mute":
        pyautogui.press("volumemute")
    speak(f"Volume {action}d.")

def process_command(command):
    """Process the voice command."""
    if not command:
        return True

    # Wake word detection
    if "hey assistant" in command:
        speak("How can I help you?")
        return True

    # File operations
    elif "create folder" in command:
        folder_name = command.replace("create folder", "").strip()
        create_folder(folder_name)
    elif "list files in" in command:
        folder_path = command.replace("list files in", "").strip()
        list_files(folder_path)
    elif "rename" in command and "to" in command:
        parts = command.split("to")
        old_name = parts[0].replace("rename", "").strip()
        new_name = parts[1].strip()
        rename_file(old_name, new_name)
    elif "copy" in command and "to" in command:
        parts = command.split("to")
        source = parts[0].replace("copy", "").strip()
        destination = parts[1].strip()
        copy_file(source, destination)

    # System control
    elif "open" in command:
        app_name = command.replace("open", "").strip()
        open_app(app_name)
    elif "shut down" in command and authenticate():
        speak("Shutting down the system.")
        os.system("shutdown /s /t 1")
    elif "restart" in command and authenticate():
        speak("Restarting the system.")
        os.system("shutdown /r /t 1")
    elif "increase volume" in command:
        adjust_volume("increase")
    elif "decrease volume" in command:
        adjust_volume("decrease")
    elif "mute" in command:
        adjust_volume("mute")

    # Reminders
    elif "remind me to" in command:
        reminder_text = command.split("to")[1].strip()
        speak("When should I remind you?")
        reminder_time = listen()
        set_reminder(reminder_text, reminder_time)

    # Exit
    elif "exit" in command:
        speak("Goodbye!")
        return False

    else:
        speak("I didn't understand that command.")
    return True

def main():
    """Main loop."""
    speak("Hello! Say 'Hello Boss' to start.")
    running = True
    while running:
        command = listen()
        if command:
            running = process_command(command)
        root.update()

if __name__ == "__main__":
    main()
    root.mainloop()
