import tkinter as tk
from tkinter import ttk, scrolledtext


class ReportsFrame(ttk.Frame):
    def __init__(self, parent, library):
        super().__init__(parent)
        self.library = library
        self.create_widgets()
    
    def create_widgets(self):
        # Left side - Report options
        left_frame = ttk.Frame(self)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(left_frame, text="Select Report", font=("Arial", 12, "bold")).pack(pady=10)
        
        ttk.Button(left_frame, text="Most Borrowed Books", 
                  command=self.show_most_borrowed, width=25).pack(pady=5)
        ttk.Button(left_frame, text="Active Members", 
                  command=self.show_active_members, width=25).pack(pady=5)
        ttk.Button(left_frame, text="Overdue Books", 
                  command=self.show_overdue_books, width=25).pack(pady=5)
        ttk.Button(left_frame, text="Fine Revenue", 
                  command=self.show_fine_revenue, width=25).pack(pady=5)
        ttk.Button(left_frame, text="Books by Category", 
                  command=self.show_books_by_category, width=25).pack(pady=5)
        
        # Right side - Report display
        right_frame = ttk.Frame(self)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(right_frame, text="Report Output", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Text widget with scrollbar
        self.report_text = scrolledtext.ScrolledText(right_frame, width=80, height=35, 
                                                     font=("Courier", 10))
        self.report_text.pack(fill=tk.BOTH, expand=True)
    
    def clear_report(self):
        self.report_text.delete(1.0, tk.END)
    
    def display_report(self, title, content):
        self.clear_report()
        self.report_text.insert(tk.END, f"{'='*60}\n")
        self.report_text.insert(tk.END, f"{title}\n")
        self.report_text.insert(tk.END, f"{'='*60}\n\n")
        self.report_text.insert(tk.END, content)
    
    def show_most_borrowed(self):
        books = self.library.generate_most_borrowed_report(10)
        
        if not books:
            self.display_report("Most Borrowed Books", "No books found.")
            return
        
        content = ""
        for i, book in enumerate(books, 1):
            content += f"{i}. {book.get_title()}\n"
            content += f"   Author: {book.get_author()}\n"
            content += f"   Times Borrowed: {book.get_total_borrows()}\n"
            content += f"   Category: {book.get_category()}\n\n"
        
        self.display_report("Top 10 Most Borrowed Books", content)
    
    def show_active_members(self):
        report = self.library.generate_active_members_report()
        self.display_report("Active Members Report", report)
    
    def show_overdue_books(self):
        report = self.library.generate_overdue_report()
        self.display_report("Overdue Books Report", report)
    
    def show_fine_revenue(self):
        report = self.library.generate_fine_revenue_report()
        self.display_report("Fine Revenue Report", report)
    
    def show_books_by_category(self):
        report = self.library.generate_category_report()
        self.display_report("Books by Category Report", report)