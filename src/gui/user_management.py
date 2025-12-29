import tkinter as tk
from tkinter import ttk, messagebox


class UserManagementFrame(ttk.Frame):
    def __init__(self, parent, library, auth_system):
        super().__init__(parent)
        self.library = library
        self.auth_system = auth_system
        self.create_widgets()
        self.refresh_user_list()
    
    def create_widgets(self):
        # Left side - User list
        left_frame = ttk.Frame(self)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(left_frame, text="User List", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Treeview
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Email", "Role", "Active"), 
                                show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Role", text="Role")
        self.tree.heading("Active", text="Active")
        
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Email", width=200)
        self.tree.column("Role", width=100)
        self.tree.column("Active", width=80)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.on_user_select)
        
        # Right side - Add User
        right_frame = ttk.Frame(self)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Label(right_frame, text="Add New User", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Role selection
        ttk.Label(right_frame, text="User Type:").pack(pady=5)
        self.role_var = tk.StringVar(value="member")
        role_frame = ttk.Frame(right_frame)
        role_frame.pack(pady=5)
        ttk.Radiobutton(role_frame, text="Admin", variable=self.role_var, 
                       value="admin", command=self.on_role_change).pack(side=tk.LEFT)
        ttk.Radiobutton(role_frame, text="Librarian", variable=self.role_var, 
                       value="librarian", command=self.on_role_change).pack(side=tk.LEFT)
        ttk.Radiobutton(role_frame, text="Member", variable=self.role_var, 
                       value="member", command=self.on_role_change).pack(side=tk.LEFT)
        
        # Form
        self.form_frame = ttk.Frame(right_frame)
        self.form_frame.pack(fill=tk.X, pady=5)
        
        self.create_form_fields()
        
        # Buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Add User", command=self.add_user).pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form).pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Delete Selected User", command=self.delete_user).pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Refresh List", command=self.refresh_user_list).pack(fill=tk.X, pady=5)
    
    def create_form_fields(self):
        # Clear existing fields
        for widget in self.form_frame.winfo_children():
            widget.destroy()
        
        role = self.role_var.get()
        
        # Common fields
        ttk.Label(self.form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(self.form_frame, width=25)
        self.name_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(self.form_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(self.form_frame, width=25)
        self.email_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(self.form_frame, text="Phone:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.phone_entry = ttk.Entry(self.form_frame, width=25)
        self.phone_entry.grid(row=2, column=1, pady=5)
        
        row = 3
        
        # Role-specific fields
        if role == "admin":
            ttk.Label(self.form_frame, text="Admin Level:").grid(row=row, column=0, sticky=tk.W, pady=5)
            self.extra_entry = ttk.Entry(self.form_frame, width=25)
            self.extra_entry.grid(row=row, column=1, pady=5)
            row += 1
        elif role == "librarian":
            ttk.Label(self.form_frame, text="Employee ID:").grid(row=row, column=0, sticky=tk.W, pady=5)
            self.extra_entry = ttk.Entry(self.form_frame, width=25)
            self.extra_entry.grid(row=row, column=1, pady=5)
            row += 1
            
            ttk.Label(self.form_frame, text="Shift:").grid(row=row, column=0, sticky=tk.W, pady=5)
            self.shift_entry = ttk.Entry(self.form_frame, width=25)
            self.shift_entry.grid(row=row, column=1, pady=5)
            row += 1
        
        # Login credentials
        ttk.Label(self.form_frame, text="Username:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.username_entry = ttk.Entry(self.form_frame, width=25)
        self.username_entry.grid(row=row, column=1, pady=5)
        row += 1
        
        ttk.Label(self.form_frame, text="Password:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(self.form_frame, width=25, show="*")
        self.password_entry.grid(row=row, column=1, pady=5)
    
    def on_role_change(self):
        self.create_form_fields()
    
    def refresh_user_list(self):
        # Clear treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add users
        users = self.library.get_all_users()
        for user in users:
            active = "Yes" if user.get_is_active() else "No"
            self.tree.insert("", tk.END, values=(
                user.get_person_id(),
                user.get_name(),
                user.get_email(),
                user.get_role(),
                active
            ))
    
    def add_user(self):
        role = self.role_var.get()
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not all([name, email, phone, username, password]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        success = False
        message = ""
        
        if role == "admin":
            admin_level = self.extra_entry.get().strip()
            if not admin_level:
                messagebox.showerror("Error", "Admin level is required")
                return
            success, message = self.library.add_admin(name, email, phone, admin_level)
        elif role == "librarian":
            employee_id = self.extra_entry.get().strip()
            shift = self.shift_entry.get().strip()
            if not all([employee_id, shift]):
                messagebox.showerror("Error", "Employee ID and Shift are required")
                return
            success, message = self.library.add_librarian(name, email, phone, employee_id, shift)
        else:  # member
            success, message = self.library.add_member(name, email, phone)
        
        if success:
            # Add credentials
            user_id = int(message.split("ID: ")[1])
            auth_success, auth_message = self.auth_system.add_user_credentials(
                username, password, role, user_id
            )
            messagebox.showinfo("Success", f"{message}\n{auth_message}")
            self.clear_form()
            self.refresh_user_list()
        else:
            messagebox.showerror("Error", message)
    
    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        if hasattr(self, 'extra_entry'):
            self.extra_entry.delete(0, tk.END)
        if hasattr(self, 'shift_entry'):
            self.shift_entry.delete(0, tk.END)
    
    def on_user_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            user_id = item['values'][0]
            user = self.library.get_user_by_id(user_id)
            if user:
                messagebox.showinfo("User Details", user.display_info())
    
    def delete_user(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a user to delete")
            return
        
        item = self.tree.item(selection[0])
        user_id = item['values'][0]
        user_name = item['values'][1]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete user:\n{user_name} (ID: {user_id})?"):
            success, message = self.library.remove_user(user_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_user_list()
            else:
                messagebox.showerror("Error", message)