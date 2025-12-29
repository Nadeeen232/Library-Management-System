import tkinter as tk
from tkinter import ttk, messagebox
from gui.book_management import BookManagementFrame
from gui.user_management import UserManagementFrame
from gui.transaction_management import TransactionManagementFrame
from gui.reports import ReportsFrame


class AdminWindow:
    def __init__(self, parent, library, auth_system, on_logout):
        self.parent = parent
        self.library = library
        self.auth_system = auth_system
        self.on_logout = on_logout
        
        self.parent.title("Library Management System - Admin Dashboard")
        self.parent.geometry("1000x700")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Top bar
        top_frame = ttk.Frame(self.parent)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(top_frame, text=f"Logged in as: {self.auth_system.get_current_user()} (Admin)", 
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        
        ttk.Button(top_frame, text="Logout", command=self.handle_logout).pack(side=tk.RIGHT)
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create tabs
        book_frame = BookManagementFrame(self.notebook, self.library)
        user_frame = UserManagementFrame(self.notebook, self.library, self.auth_system)
        transaction_frame = TransactionManagementFrame(self.notebook, self.library)
        reports_frame = ReportsFrame(self.notebook, self.library)
        
        self.notebook.add(book_frame, text="Books")
        self.notebook.add(user_frame, text="Users")
        self.notebook.add(transaction_frame, text="Transactions")
        self.notebook.add(reports_frame, text="Reports")
    
    def handle_logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.on_logout()