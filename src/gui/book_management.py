import tkinter as tk
from tkinter import ttk, messagebox


class BookManagementFrame(ttk.Frame):
    def __init__(self, parent, library):
        super().__init__(parent)
        self.library = library
        self.create_widgets()
        self.refresh_book_list()
    
    def create_widgets(self):
        # Left side - Book list
        left_frame = ttk.Frame(self)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(left_frame, text="Book List", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Search
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_books).pack(side=tk.LEFT)
        ttk.Button(search_frame, text="Show All", command=self.refresh_book_list).pack(side=tk.LEFT, padx=2)
        
        # Treeview
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Title", "Author", "Category", "Available"), 
                                show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Available", text="Available")
        
        self.tree.column("ID", width=50)
        self.tree.column("Title", width=200)
        self.tree.column("Author", width=150)
        self.tree.column("Category", width=100)
        self.tree.column("Available", width=80)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.on_book_select)
        
        # Right side - Add/Edit Book
        right_frame = ttk.Frame(self)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Label(right_frame, text="Add New Book", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Form
        form_frame = ttk.Frame(right_frame)
        form_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.title_entry = ttk.Entry(form_frame, width=25)
        self.title_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(form_frame, text="Author:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.author_entry = ttk.Entry(form_frame, width=25)
        self.author_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(form_frame, text="ISBN:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.isbn_entry = ttk.Entry(form_frame, width=25)
        self.isbn_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(form_frame, text="Category:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.category_entry = ttk.Entry(form_frame, width=25)
        self.category_entry.grid(row=3, column=1, pady=5)
        
        ttk.Label(form_frame, text="Year:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.year_entry = ttk.Entry(form_frame, width=25)
        self.year_entry.grid(row=4, column=1, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Add Book", command=self.add_book).pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form).pack(fill=tk.X, pady=5)
    
    def refresh_book_list(self):
        # Clear treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add books
        books = self.library.get_all_books()
        for book in books:
            available = "Yes" if book.get_is_available() else "No"
            self.tree.insert("", tk.END, values=(
                book.get_book_id(),
                book.get_title(),
                book.get_author(),
                book.get_category(),
                available
            ))
    
    def search_books(self):
        search_term = self.search_entry.get().strip()
        if not search_term:
            self.refresh_book_list()
            return
        
        # Clear treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Search by title
        books = self.library.search_books_by_title(search_term)
        for book in books:
            available = "Yes" if book.get_is_available() else "No"
            self.tree.insert("", tk.END, values=(
                book.get_book_id(),
                book.get_title(),
                book.get_author(),
                book.get_category(),
                available
            ))
    
    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        isbn = self.isbn_entry.get().strip()
        category = self.category_entry.get().strip()
        year = self.year_entry.get().strip()
        
        if not all([title, author, isbn, category, year]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        success, message = self.library.add_book(title, author, isbn, category, year)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.refresh_book_list()
        else:
            messagebox.showerror("Error", message)
    
    def clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.isbn_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
    
    def on_book_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            book_id = item['values'][0]
            book = self.library.get_book_by_id(book_id)
            if book:
                details = f"Book Details:\n\n"
                details += f"ID: {book.get_book_id()}\n"
                details += f"Title: {book.get_title()}\n"
                details += f"Author: {book.get_author()}\n"
                details += f"ISBN: {book.get_isbn()}\n"
                details += f"Category: {book.get_category()}\n"
                details += f"Year: {book.get_publication_year()}\n"
                details += f"Available: {'Yes' if book.get_is_available() else 'No'}\n"
                details += f"Total Borrows: {book.get_total_borrows()}"
                messagebox.showinfo("Book Details", details)