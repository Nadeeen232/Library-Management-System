import tkinter as tk
from tkinter import ttk, messagebox
from gui.book_management import BookManagementFrame
from gui.transaction_management import TransactionManagementFrame
from gui.reports import ReportsFrame


class LibrarianWindow:
    def __init__(self, parent, library, auth_system, on_logout):
        self.parent = parent
        self.library = library
        self.auth_system = auth_system
        self.on_logout = on_logout
        
        self.parent.title("Library Management System - Librarian Dashboard")
        self.parent.geometry("1000x700")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Top bar
        top_frame = ttk.Frame(self.parent)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(top_frame, text=f"Logged in as: {self.auth_system.get_current_user()} (Librarian)", 
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        
        ttk.Button(top_frame, text="Logout", command=self.handle_logout).pack(side=tk.RIGHT)
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create tabs (Librarian can't manage users)
        book_frame = BookManagementFrame(self.notebook, self.library)
        transaction_frame = TransactionManagementFrame(self.notebook, self.library)
        reports_frame = ReportsFrame(self.notebook, self.library)
        
        self.notebook.add(book_frame, text="Books")
        self.notebook.add(transaction_frame, text="Transactions")
        self.notebook.add(reports_frame, text="Reports")
    
    def handle_logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.on_logout()


# src/gui/member_window.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext


class MemberWindow:
    def __init__(self, parent, library, auth_system, on_logout):
        self.parent = parent
        self.library = library
        self.auth_system = auth_system
        self.on_logout = on_logout
        
        # Get member info
        credentials = self.auth_system.load_credentials()
        username = self.auth_system.get_current_user()
        member_id = credentials[username]["user_id"]
        self.member = self.library.get_user_by_id(member_id)
        
        if not self.member:
            messagebox.showerror("Error", "Member account not found!")
            self.on_logout()
            return
        
        self.parent.title("Library Management System - Member Portal")
        self.parent.geometry("900x600")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Top bar
        top_frame = ttk.Frame(self.parent)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(top_frame, text=f"Welcome, {self.member.get_name()}", 
                 font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        
        ttk.Button(top_frame, text="Logout", command=self.handle_logout).pack(side=tk.RIGHT)
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create tabs
        search_frame = self.create_search_tab()
        borrowed_frame = self.create_borrowed_books_tab()
        account_frame = self.create_account_tab()
        
        self.notebook.add(search_frame, text="Search Books")
        self.notebook.add(borrowed_frame, text="My Books")
        self.notebook.add(account_frame, text="My Account")
    
    def create_search_tab(self):
        frame = ttk.Frame(self.notebook)
        
        # Search controls
        search_frame = ttk.Frame(frame)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_books).pack(side=tk.LEFT)
        ttk.Button(search_frame, text="Show All", command=self.show_all_books).pack(side=tk.LEFT, padx=5)
        
        # Results tree
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.search_tree = ttk.Treeview(tree_frame, 
                                       columns=("ID", "Title", "Author", "Category", "Available"), 
                                       show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.search_tree.yview)
        
        self.search_tree.heading("ID", text="ID")
        self.search_tree.heading("Title", text="Title")
        self.search_tree.heading("Author", text="Author")
        self.search_tree.heading("Category", text="Category")
        self.search_tree.heading("Available", text="Available")
        
        self.search_tree.column("ID", width=50)
        self.search_tree.column("Title", width=250)
        self.search_tree.column("Author", width=200)
        self.search_tree.column("Category", width=150)
        self.search_tree.column("Available", width=100)
        
        self.search_tree.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="To borrow a book, please contact the librarian with the Book ID", 
                 font=("Arial", 9, "italic")).pack(pady=5)
        
        return frame
    
    def create_borrowed_books_tab(self):
        frame = ttk.Frame(self.notebook)
        
        ttk.Label(frame, text="My Borrowed Books", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        # Tree
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.borrowed_tree = ttk.Treeview(tree_frame, 
                                         columns=("ID", "Title", "Author", "Due Date", "Status"), 
                                         show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.borrowed_tree.yview)
        
        self.borrowed_tree.heading("ID", text="Book ID")
        self.borrowed_tree.heading("Title", text="Title")
        self.borrowed_tree.heading("Author", text="Author")
        self.borrowed_tree.heading("Due Date", text="Due Date")
        self.borrowed_tree.heading("Status", text="Status")
        
        self.borrowed_tree.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(frame, text="Refresh", command=self.refresh_borrowed_books).pack(pady=10)
        
        self.refresh_borrowed_books()
        
        return frame
    
    def create_account_tab(self):
        frame = ttk.Frame(self.notebook)
        
        ttk.Label(frame, text="Account Information", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        info_frame = ttk.Frame(frame)
        info_frame.pack(padx=20, pady=20)
        
        info_text = scrolledtext.ScrolledText(info_frame, width=60, height=15, 
                                              font=("Courier", 10))
        info_text.pack()
        
        info_text.insert(tk.END, self.member.display_info())
        info_text.config(state=tk.DISABLED)
        
        return frame
    
    def search_books(self):
        search_term = self.search_entry.get().strip()
        
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        
        if search_term:
            books = self.library.search_books_by_title(search_term)
        else:
            books = self.library.get_available_books()
        
        for book in books:
            available = "Yes ✓" if book.get_is_available() else "No ✗"
            self.search_tree.insert("", tk.END, values=(
                book.get_book_id(),
                book.get_title(),
                book.get_author(),
                book.get_category(),
                available
            ))
    
    def show_all_books(self):
        self.search_entry.delete(0, tk.END)
        
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        
        books = self.library.get_available_books()
        for book in books:
            self.search_tree.insert("", tk.END, values=(
                book.get_book_id(),
                book.get_title(),
                book.get_author(),
                book.get_category(),
                "Yes ✓"
            ))
    
    def refresh_borrowed_books(self):
        for item in self.borrowed_tree.get_children():
            self.borrowed_tree.delete(item)
        
        member_id = self.member.get_person_id()
        books = self.library.get_member_borrowed_books(member_id)
        transactions = self.library.get_member_transactions(member_id)
        
        for book in books:
            due_date = "N/A"
            status = "Borrowed"
            
            for trans in transactions:
                if (trans.get_book_id() == book.get_book_id() and 
                    trans.get_transaction_type() == "borrow" and 
                    trans.get_return_date() is None):
                    due_date = trans.get_due_date()
                    if trans.is_overdue():
                        status = f"OVERDUE ({trans.get_days_overdue()} days)"
                    break
            
            self.borrowed_tree.insert("", tk.END, values=(
                book.get_book_id(),
                book.get_title(),
                book.get_author(),
                due_date,
                status
            ))
    
    def handle_logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.on_logout()