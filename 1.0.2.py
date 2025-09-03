import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3

# Database setup
class Database:
    def __init__(self):
        self.conn = sqlite3.connect("user_data.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def create_account(self, username, password):
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def login(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        return self.cursor.fetchone() is not None

    def __del__(self):
        self.conn.close()

# Main timer app
class TimerApp:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.night_mode = False
        self.build_login_ui()

    def toggle_night_mode(self):
        self.night_mode = not self.night_mode
        bg = "#2e2e2e" if self.night_mode else "#c6d4c6"
        fg = "#ffffff" if self.night_mode else "#000000"
        self.root.configure(bg=bg)
        self.top_frame.configure(bg=bg)
        self.bottom_frame.configure(bg=bg)
        self.date_time_label.configure(bg=bg, fg=fg)

    def build_login_ui(self):
        self.root.title("D-timer")
        self.root.geometry("600x400")
        self.root.configure(bg="#c6d4c6")

        self.top_frame = tk.Frame(self.root, bg="#c6d4c6")
        self.top_frame.pack(fill='x', pady=10, padx=20)

        self.bottom_frame = tk.Frame(self.root, bg="#c6d4c6")
        self.bottom_frame.pack(pady=50)

        self.date_time_label = tk.Label(self.top_frame, text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), bg="#c6d4c6")
        self.date_time_label.pack(side="right")

        # Night mode button
        self.night_mode_btn = tk.Button(self.top_frame, text="Night Mode On/Off", command=self.toggle_night_mode)
        self.night_mode_btn.pack(side="left")

        # Login UI elements
        tk.Label(self.bottom_frame, text="Username:").grid(row=0, column=0, sticky="e")
        self.username_entry = tk.Entry(self.bottom_frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.bottom_frame, text="Password:").grid(row=1, column=0, sticky="e")
        self.password_entry = tk.Entry(self.bottom_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_btn = tk.Button(self.bottom_frame, text="Login", command=self.handle_login)
        self.login_btn.grid(row=2, column=0, columnspan=2, pady=5)

        self.create_btn = tk.Button(self.bottom_frame, text="Create Account", command=self.handle_create_account)
        self.create_btn.grid(row=3, column=0, columnspan=2)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.db.login(username, password):
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.show_timer_screen()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    def handle_create_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.db.create_account(username, password):
            messagebox.showinfo("Account Created", "Account successfully created.")
        else:
            messagebox.showerror("Error", "Username already exists.")

    def show_timer_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#c6d4c6")

        self.timer_label = tk.Label(self.root, text="00:00:00", font=("Helvetica", 48), bg="#c6d4c6")
        self.timer_label.pack(pady=20)

        self.start_btn = tk.Button(self.root, text="Start", command=self.start_timer)
        self.start_btn.pack(side="left", padx=10)

        self.pause_btn = tk.Button(self.root, text="Pause", command=self.pause_timer)
        self.pause_btn.pack(side="left", padx=10)

        self.reset_btn = tk.Button(self.root, text="Reset", command=self.reset_timer)
        self.reset_btn.pack(side="left", padx=10)

        self.running = False
        self.counter = 0

    def update_timer(self):
        if self.running:
            self.counter += 1
            time_str = self.format_time(self.counter)
            self.timer_label.config(text=time_str)
            self.root.after(1000, self.update_timer)

    def format_time(self, seconds):
        hrs = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hrs:02}:{mins:02}:{secs:02}"

    def start_timer(self):
        if not self.running:
            self.running = True
            self.update_timer()

    def pause_timer(self):
        self.running = False

    def reset_timer(self):
        self.running = False
        self.counter = 0
        self.timer_label.config(text="00:00:00")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
