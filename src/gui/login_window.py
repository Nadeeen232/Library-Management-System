import tkinter as tk
from tkinter import ttk, messagebox


class LoginWindow:
    def __init__(self, parent, auth_system, on_success):
        self.parent = parent
        self.auth_system = auth_system
        self.on_success = on_success
        
        self.parent.title("Library Management System - Login")
        self.parent.geometry("400x350")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.parent, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Library Management System", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        subtitle_label = ttk.Label(main_frame, text="Please login to continue", 
                                   font=("Arial", 10))
        subtitle_label.pack(pady=5)
        
        # Login form frame
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20)
        
        # Username
        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=10)
        self.username_entry = ttk.Entry(form_frame, width=25)
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Password
        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.password_entry = ttk.Entry(form_frame, width=25, show="*")
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Login button
        login_btn = ttk.Button(main_frame, text="Login", command=self.handle_login)
        login_btn.pack(pady=20)
        
        # Default credentials info
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(pady=10)
        
        ttk.Label(info_frame, text="Default Credentials:", 
                 font=("Arial", 9, "bold")).pack()
        ttk.Label(info_frame, text="Admin: admin / admin123", 
                 font=("Arial", 8)).pack()
        ttk.Label(info_frame, text="Librarian: librarian / lib123", 
                 font=("Arial", 8)).pack()
        
        # Bind Enter key
        self.username_entry.bind("<Return>", lambda e: self.handle_login())
        self.password_entry.bind("<Return>", lambda e: self.handle_login())
        
        # Focus on username
        self.username_entry.focus()
    
    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        if self.auth_system.login(username, password):
            messagebox.showinfo("Success", f"Welcome {username}!")
            self.on_success()
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.password_entry.delete(0, tk.END)