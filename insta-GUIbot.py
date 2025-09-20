import threading
import time
from tkinter import *
from tkinter import ttk, messagebox
from instabot import Bot
import pyttsx3
from plyer import notification
from getpass import getpass

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def notify(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=5
    )

class InstagramBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Follow Request Bot")
        self.root.geometry("700x700")
        self.root.configure(bg="#1e1e2f")

        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", font=("Helvetica", 12), padding=6)
        style.configure("TLabel", background="#1e1e2f", foreground="white", font=("Helvetica", 12))
        style.configure("Header.TLabel", font=("Helvetica", 16, "bold"))

        # Header
        self.header = ttk.Label(root, text="Instagram Follow Request Bot", style="Header.TLabel")
        self.header.pack(pady=10)

        # Username
        self.username_label = ttk.Label(root, text="Instagram Username:")
        self.username_label.pack(pady=5)
        self.username_entry = ttk.Entry(root, width=30)
        self.username_entry.pack()

        # Password
        self.password_label = ttk.Label(root, text="Instagram Password:")
        self.password_label.pack(pady=5)
        self.password_entry = ttk.Entry(root, width=30, show="*")
        self.password_entry.pack()

        # Target user
        self.target_label = ttk.Label(root, text="Target Username:")
        self.target_label.pack(pady=5)
        self.target_entry = ttk.Entry(root, width=30)
        self.target_entry.pack()

        # Interval
        self.interval_label = ttk.Label(root, text="Check Interval (seconds):")
        self.interval_label.pack(pady=5)
        self.interval_entry = ttk.Entry(root, width=10)
        self.interval_entry.insert(0, "60")
        self.interval_entry.pack()

        # Status box
        self.status_text = Text(root, height=6, width=50, bg="#2e2e3e", fg="white", state=DISABLED)
        self.status_text.pack(pady=10)

        # Start button
        self.start_button = ttk.Button(root, text="Start Sending Requests", command=self.start_bot_thread)
        self.start_button.pack(pady=5)

        # Stop flag
        self.stop_flag = False

        # Animate background color
        self.colors = ["#1e1e2f", "#2e2e3e", "#3e3e4e", "#4e4e5e"]
        self.color_index = 0
        self.animate_bg()

    def animate_bg(self):
        self.root.configure(bg=self.colors[self.color_index])
        self.color_index = (self.color_index + 1) % len(self.colors)
        self.root.after(1000, self.animate_bg)

    def log_status(self, message):
        self.status_text.config(state=NORMAL)
        self.status_text.insert(END, message + "\n")
        self.status_text.see(END)
        self.status_text.config(state=DISABLED)
        speak(message)
        notify("Instagram Bot", message)

    def start_bot_thread(self):
        # Disable start button to prevent multiple threads
        self.start_button.config(state=DISABLED)
        self.stop_flag = False
        thread = threading.Thread(target=self.send_friend_request)
        thread.daemon = True
        thread.start()

    def send_friend_request(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        target_user = self.target_entry.get().strip()
        try:
            check_interval = int(self.interval_entry.get().strip())
        except ValueError:
            self.log_status("Invalid interval. Please enter a number.")
            self.start_button.config(state=NORMAL)
            return

        if not username or not password or not target_user:
            self.log_status("Please fill all fields.")
            self.start_button.config(state=NORMAL)
            return

        bot = Bot()
        try:
            self.log_status("Logging in...")
            bot.login(username=username, password=password)
            self.log_status("Logged in successfully.")

            target_user_id = bot.get_user_id_from_username(target_user)
            if not target_user_id:
                self.log_status("Target user not found.")
                bot.logout()
                self.start_button.config(state=NORMAL)
                return

            while not self.stop_flag:
                bot.follow(target_user)
                self.log_status(f"Sent follow request to {target_user}.")

                self.log_status(f"Waiting {check_interval} seconds before checking status...")
                for _ in range(check_interval):
                    if self.stop_flag:
                        break
                    time.sleep(1)
                if self.stop_flag:
                    break

                following = bot.get_user_following(bot.user_id)
                if target_user_id in following:
                    self.log_status("Request accepted successfully!")
                    break

                try:
                    user_info = bot.get_user_info(target_user_id)
                    if user_info is None:
                        self.log_status("User  has blocked you or does not exist.")
                        break
                except Exception:
                    self.log_status("User  has blocked you or does not exist.")
                    break

                self.log_status("Request not accepted yet. Retrying...")

        except Exception as e:
            self.log_status(f"Error: {e}")

        finally:
            bot.logout()
            self.log_status("Logged out.")
            self.start_button.config(state=NORMAL)

    def stop(self):
        self.stop_flag = True
        self.log_status("Stopping bot...")

if __name__ == "__main__":
    root = Tk()
    app = InstagramBotGUI(root)

    # Add a stop button to allow user to stop the bot gracefully
    stop_button = ttk.Button(root, text="Stop", command=app.stop)
    stop_button.pack(pady=5)

    root.mainloop()
