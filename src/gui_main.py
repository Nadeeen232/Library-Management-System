import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import tkinter as tk
from tkinter import ttk, messagebox
from controllers.library import Library
from utils.auth import AuthSystem
from gui.login_window import LoginWindow
from gui.admin_window import AdminWindow
from gui.librarian_window import LibrarianWindow
from gui.member_window import MemberWindow


class LibraryGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Library Management System")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Center window on screen
        self.center_window(self.root, 400, 300)
        
        # Initialize systems
        self.library = Library()
        self.auth_system = AuthSystem()
        
        # Show login window
        self.show_login()
        
    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def show_login(self):
        LoginWindow(self.root, self.auth_system, self.on_login_success)
    
    def on_login_success(self):
        # Close login window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Open appropriate window based on role
        role = self.auth_system.get_current_role()
        
        if role == "admin":
            AdminWindow(self.root, self.library, self.auth_system, self.on_logout)
        elif role == "librarian":
            LibrarianWindow(self.root, self.library, self.auth_system, self.on_logout)
        elif role == "member":
            MemberWindow(self.root, self.library, self.auth_system, self.on_logout)
    
    def on_logout(self):
        self.auth_system.logout()
        for widget in self.root.winfo_children():
            widget.destroy()
        self.show_login()
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = LibraryGUI()
    app.run()