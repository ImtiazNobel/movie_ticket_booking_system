import tkinter as tk
from tkinter import messagebox
import sqlite3


class MovieBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Ticket Booking System")
        self.db_connection = sqlite3.connect("movie_booking.db")
        self.db_cursor = self.db_connection.cursor()

        # Create necessary tables if they don't exist
        self.create_tables()

        # Call the login screen initially
        self.login_screen()

    def create_tables(self):
        # Create Users table
        self.db_cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
        ''')

        # Create Hall table
        self.db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS halls (
            hall_no TEXT PRIMARY KEY,
            rows INTEGER,
            cols INTEGER
        )
        ''')

        # Create Shows table
        self.db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS shows (
            show_id TEXT PRIMARY KEY,
            hall_no TEXT,
            movie_name TEXT,
            show_time TEXT,
            FOREIGN KEY(hall_no) REFERENCES halls(hall_no)
        )
        ''')

        # Create Seats table
        self.db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS seats (
            hall_no TEXT,
            show_id TEXT,
            row INTEGER,
            col INTEGER,
            status TEXT,  -- 'free' or 'booked'
            PRIMARY KEY (hall_no, show_id, row, col),
            FOREIGN KEY(hall_no) REFERENCES halls(hall_no),
            FOREIGN KEY(show_id) REFERENCES shows(show_id)
        )
        ''')

        self.db_connection.commit()

    def login_screen(self):
        self.clear_frame()

        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Username:").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="Password:").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def authenticate():
            username = username_entry.get()
            password = password_entry.get()

            # Hardcoded admin credentials
            admin_username = "admin"
            admin_password = "admin123"

            if username == admin_username and password == admin_password:
                messagebox.showinfo("Login Successful", "Welcome, Admin!")
                self.main_screen(admin=True)
            else:
                self.db_cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
                user = self.db_cursor.fetchone()
                if user:
                    messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                    self.main_screen(admin=False)
                else:
                    messagebox.showerror("Login Failed", "Invalid credentials!")

        def register_user():
            self.register_screen()

        tk.Button(self.root, text="Login", command=authenticate).pack(pady=10)
        tk.Button(self.root, text="Register", command=register_user).pack(pady=5)

    def register_screen(self):
        self.clear_frame()

        tk.Label(self.root, text="Register", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="New Username:").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="New Password:").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def register():
            username = username_entry.get()
            password = password_entry.get()

            if username and password:
                try:
                    self.db_cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                    self.db_connection.commit()
                    messagebox.showinfo("Success", "Registration successful!")
                    self.login_screen()
                except sqlite3.IntegrityError:
                    messagebox.showerror("Error", "Username already exists!")
            else:
                messagebox.showerror("Error", "Fields cannot be empty!")

        tk.Button(self.root, text="Register", command=register).pack(pady=10)
        tk.Button(self.root, text="Back to Login", command=self.login_screen).pack()

    def main_screen(self, admin):
        self.clear_frame()

        tk.Label(self.root, text="Welcome to Star Cinema", font=("Arial", 16)).pack(pady=10)

        if admin:
            tk.Button(self.root, text="Add Hall", command=self.add_hall_screen, width=20).pack(pady=5)
            tk.Button(self.root, text="Add Show", command=self.add_show_screen, width=20).pack(pady=5)
            tk.Button(self.root, text="View Shows", command=self.view_shows_screen_admin, width=20).pack(pady=5)
            tk.Button(self.root, text="Exit to Login", command=self.login_screen, width=20).pack(pady=5)
        else:
            tk.Button(self.root, text="Book Seats", command=self.book_seats_screen, width=20).pack(pady=5)
            tk.Button(self.root, text="View Available Seats", command=self.view_available_seats_screen, width=20).pack(pady=5)
            tk.Button(self.root, text="View Shows", command=self.view_shows_screen_user, width=20).pack(pady=5)

        tk.Button(self.root, text="Logout", command=self.login_screen, width=20).pack(pady=5)

    def add_hall_screen(self):
        self.clear_frame()
        tk.Label(self.root, text="Add Hall", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Hall Number:").pack()
        hall_no_entry = tk.Entry(self.root)
        hall_no_entry.pack()

        tk.Label(self.root, text="Rows:").pack()
        rows_entry = tk.Entry(self.root)
        rows_entry.pack()

        tk.Label(self.root, text="Columns:").pack()
        cols_entry = tk.Entry(self.root)
        cols_entry.pack()

        def add_hall():
            hall_no = hall_no_entry.get()
            rows = rows_entry.get()
            cols = cols_entry.get()

            if hall_no and rows.isdigit() and cols.isdigit():
                try:
                    self.db_cursor.execute("INSERT INTO halls (hall_no, rows, cols) VALUES (?, ?, ?)",
                                           (hall_no, int(rows), int(cols)))
                    self.db_connection.commit()
                    messagebox.showinfo("Success", "Hall added successfully!")
                    self.main_screen(admin=True)
                except sqlite3.IntegrityError:
                    messagebox.showerror("Error", "Hall number already exists!")
            else:
                messagebox.showerror("Error", "Invalid input!")

        tk.Button(self.root, text="Add", command=add_hall).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.main_screen(admin=True)).pack()

    def add_show_screen(self):
        self.clear_frame()
        tk.Label(self.root, text="Add Show", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Show ID:").pack()
        show_id_entry = tk.Entry(self.root)
        show_id_entry.pack()

        tk.Label(self.root, text="Hall Number:").pack()
        hall_no_entry = tk.Entry(self.root)
        hall_no_entry.pack()

        tk.Label(self.root, text="Movie Name:").pack()
        movie_name_entry = tk.Entry(self.root)
        movie_name_entry.pack()

        tk.Label(self.root, text="Show Time:").pack()
        show_time_entry = tk.Entry(self.root)
        show_time_entry.pack()

        def add_show():
            show_id = show_id_entry.get()
            hall_no = hall_no_entry.get()
            movie_name = movie_name_entry.get()
            show_time = show_time_entry.get()

            if show_id and hall_no and movie_name and show_time:
                try:
                    self.db_cursor.execute("INSERT INTO shows (show_id, hall_no, movie_name, show_time) VALUES (?, ?, ?, ?)",
                                           (show_id, hall_no, movie_name, show_time))
                    self.db_connection.commit()

                    # Initialize seats for this show
                    self.db_cursor.execute("SELECT rows, cols FROM halls WHERE hall_no = ?", (hall_no,))
                    hall = self.db_cursor.fetchone()
                    if hall:
                        rows, cols = hall
                        for row in range(1, rows + 1):
                            for col in range(1, cols + 1):
                                self.db_cursor.execute(
                                    "INSERT INTO seats (hall_no, show_id, row, col, status) VALUES (?, ?, ?, ?, 'free')",
                                    (hall_no, show_id, row, col))
                        self.db_connection.commit()
                        messagebox.showinfo("Success", "Show added successfully!")
                        self.main_screen(admin=True)
                    else:
                        messagebox.showerror("Error", "Invalid Hall Number!")
                except sqlite3.IntegrityError:
                    messagebox.showerror("Error", "Show ID already exists!")
            else:
                messagebox.showerror("Error", "All fields are required!")

        tk.Button(self.root, text="Add", command=add_show).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.main_screen(admin=True)).pack()

    def view_shows_screen_admin(self):
        self.clear_frame()
        tk.Label(self.root, text="Shows List (Admin)", font=("Arial", 16)).pack(pady=10)

        shows_listbox = tk.Listbox(self.root, width=50, height=10)
        shows_listbox.pack()

        self.db_cursor.execute("SELECT show_id, movie_name, show_time FROM shows")
        shows = self.db_cursor.fetchall()

        for show in shows:
            shows_listbox.insert(tk.END, f"ID: {show[0]}, Movie: {show[1]}, Time: {show[2]}")

        tk.Button(self.root, text="Back", command=lambda: self.main_screen(admin=True)).pack(pady=10)

    def view_shows_screen_user(self):
        self.clear_frame()
        tk.Label(self.root, text="Shows List (User)", font=("Arial", 16)).pack(pady=10)

        shows_listbox = tk.Listbox(self.root, width=50, height=10)
        shows_listbox.pack()

        self.db_cursor.execute("SELECT show_id, movie_name, show_time FROM shows")
        shows = self.db_cursor.fetchall()

        for show in shows:
            shows_listbox.insert(tk.END, f"ID: {show[0]}, Movie: {show[1]}, Time: {show[2]}")

        tk.Button(self.root, text="Back", command=lambda: self.main_screen(admin=False)).pack(pady=10)

    def book_seats_screen(self):
        self.clear_frame()
        tk.Label(self.root, text="Book Seats", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Select a Show:").pack()
        shows_listbox = tk.Listbox(self.root, width=70, height=10)
        shows_listbox.pack()

        self.db_cursor.execute("SELECT * FROM shows")
        shows = self.db_cursor.fetchall()
        for show in shows:
            shows_listbox.insert(tk.END, f"ID: {show[0]}, Movie: {show[2]}, Time: {show[3]}")

        def select_show():
            selected_index = shows_listbox.curselection()
            if not selected_index:
                messagebox.showerror("Error", "Please select a show!")
                return

            selected_show = shows[selected_index[0]]
            self.display_seats(selected_show[0], selected_show[1])

        tk.Button(self.root, text="Select Show", command=select_show).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.main_screen(admin=False)).pack(pady=10)

    def display_seats(self, show_id, hall_no):
        self.clear_frame()
        tk.Label(self.root, text=f"Seats for Show ID: {show_id}", font=("Arial", 16)).pack(pady=10)

        seats_frame = tk.Frame(self.root)
        seats_frame.pack()

        self.db_cursor.execute("SELECT row, col, status FROM seats WHERE show_id = ? AND hall_no = ?", (show_id, hall_no))
        seats = self.db_cursor.fetchall()

        rows = max(seat[0] for seat in seats)
        cols = max(seat[1] for seat in seats)

        buttons = {}
        for seat in seats:
            row, col, status = seat
            text = f"{row},{col}"
            color = "green" if status == "free" else "red"
            btn = tk.Button(seats_frame, text=text, bg=color, width=2, height=1)

            def book_seat(row=row, col=col):
                self.book_seat(show_id, hall_no, row, col)

            btn.config(command=book_seat)
            btn.grid(row=row, column=col, padx=2, pady=2)
            buttons[(row, col)] = btn

        tk.Button(self.root, text="Back", command=lambda: self.book_seats_screen()).pack(pady=10)

    def book_seat(self, show_id, hall_no, row, col):
        self.db_cursor.execute("UPDATE seats SET status = 'booked' WHERE show_id = ? AND hall_no = ? AND row = ? AND col = ?",
                               (show_id, hall_no, row, col))
        self.db_connection.commit()
        messagebox.showinfo("Booking Successful", f"Seat {row},{col} has been booked!")
        self.display_seats(show_id, hall_no)

    def view_available_seats_screen(self):
        self.clear_frame()
        tk.Label(self.root, text="Available Seats", font=("Arial", 16)).pack(pady=10)

        shows_listbox = tk.Listbox(self.root, width=50, height=10)
        shows_listbox.pack()

        self.db_cursor.execute("""
        SELECT s.show_id, s.movie_name, s.show_time, COUNT(seats.status)
        FROM shows s
        JOIN seats seats ON s.show_id = seats.show_id
        WHERE seats.status = 'free'
        GROUP BY s.show_id
        """)
        shows = self.db_cursor.fetchall()

        for show in shows:
            shows_listbox.insert(tk.END, f"ID: {show[0]}, Movie: {show[1]}, Time: {show[2]}, Free Seats: {show[3]}")

        tk.Button(self.root, text="Back", command=lambda: self.main_screen(admin=False)).pack(pady=10)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieBookingApp(root)
    root.mainloop()
