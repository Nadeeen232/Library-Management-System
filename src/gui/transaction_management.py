import tkinter as tk
from tkinter import ttk, messagebox


class TransactionManagementFrame(ttk.Frame):
    def __init__(self, parent, library):
        super().__init__(parent)
        self.library = library
        self.create_widgets()
        self.refresh_transaction_list()
    
    def create_widgets(self):
        # Left side - Transaction list
        left_frame = ttk.Frame(self)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(left_frame, text="Transaction History", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Treeview
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(tree_frame, 
                                columns=("ID", "Type", "Book ID", "Member ID", "Date", "Due Date"), 
                                show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading("ID", text="Trans ID")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Book ID", text="Book ID")
        self.tree.heading("Member ID", text="Member ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Due Date", text="Due Date")
        
        self.tree.column("ID", width=80)
        self.tree.column("Type", width=80)
        self.tree.column("Book ID", width=80)
        self.tree.column("Member ID", width=100)
        self.tree.column("Date", width=100)
        self.tree.column("Due Date", width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Right side - Borrow/Return
        right_frame = ttk.Frame(self)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        # Borrow Book Section
        borrow_frame = ttk.LabelFrame(right_frame, text="Borrow Book", padding=10)
        borrow_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(borrow_frame, text="Book ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.borrow_book_entry = ttk.Entry(borrow_frame, width=20)
        self.borrow_book_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(borrow_frame, text="Member ID:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.borrow_member_entry = ttk.Entry(borrow_frame, width=20)
        self.borrow_member_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(borrow_frame, text="Days:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.borrow_days_entry = ttk.Entry(borrow_frame, width=20)
        self.borrow_days_entry.insert(0, "14")
        self.borrow_days_entry.grid(row=2, column=1, pady=5)
        
        ttk.Button(borrow_frame, text="Borrow Book", 
                  command=self.borrow_book).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Return Book Section
        return_frame = ttk.LabelFrame(right_frame, text="Return Book", padding=10)
        return_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(return_frame, text="Book ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.return_book_entry = ttk.Entry(return_frame, width=20)
        self.return_book_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(return_frame, text="Member ID:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.return_member_entry = ttk.Entry(return_frame, width=20)
        self.return_member_entry.grid(row=1, column=1, pady=5)
        
        ttk.Button(return_frame, text="Return Book", 
                  command=self.return_book).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Pay Fine Section
        fine_frame = ttk.LabelFrame(right_frame, text="Pay Fine", padding=10)
        fine_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(fine_frame, text="Member ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.fine_member_entry = ttk.Entry(fine_frame, width=20)
        self.fine_member_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(fine_frame, text="Amount:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.fine_amount_entry = ttk.Entry(fine_frame, width=20)
        self.fine_amount_entry.grid(row=1, column=1, pady=5)
        
        ttk.Button(fine_frame, text="Pay Fine", 
                  command=self.pay_fine).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Refresh button
        ttk.Button(right_frame, text="Refresh List", 
                  command=self.refresh_transaction_list).pack(pady=10)
    
    def refresh_transaction_list(self):
        # Clear treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add transactions
        transactions = self.library.get_all_transactions()
        for trans in transactions:
            self.tree.insert("", tk.END, values=(
                trans.get_transaction_id(),
                trans.get_transaction_type().capitalize(),
                trans.get_book_id(),
                trans.get_member_id(),
                trans.get_transaction_date(),
                trans.get_due_date() or "N/A"
            ))
    
    def borrow_book(self):
        try:
            book_id = int(self.borrow_book_entry.get().strip())
            member_id = int(self.borrow_member_entry.get().strip())
            days = int(self.borrow_days_entry.get().strip())
            
            success, message = self.library.borrow_book(book_id, member_id, days)
            
            if success:
                messagebox.showinfo("Success", message)
                self.borrow_book_entry.delete(0, tk.END)
                self.borrow_member_entry.delete(0, tk.END)
                self.borrow_days_entry.delete(0, tk.END)
                self.borrow_days_entry.insert(0, "14")
                self.refresh_transaction_list()
            else:
                messagebox.showerror("Error", message)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
    
    def return_book(self):
        try:
            book_id = int(self.return_book_entry.get().strip())
            member_id = int(self.return_member_entry.get().strip())
            
            success, message = self.library.return_book(book_id, member_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.return_book_entry.delete(0, tk.END)
                self.return_member_entry.delete(0, tk.END)
                self.refresh_transaction_list()
            else:
                messagebox.showerror("Error", message)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
    
    def pay_fine(self):
        try:
            member_id = int(self.fine_member_entry.get().strip())
            amount = float(self.fine_amount_entry.get().strip())
            
            success, message = self.library.pay_member_fine(member_id, amount)
            
            if success:
                messagebox.showinfo("Success", message)
                self.fine_member_entry.delete(0, tk.END)
                self.fine_amount_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", message)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")