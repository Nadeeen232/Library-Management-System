from abc import ABC, abstractmethod


class Person(ABC):
    def __init__(self, person_id, name, email, phone):
        self._person_id = person_id
        self._name = name
        self._email = email
        self._phone = phone
        self._is_active = True
    
    def get_person_id(self):
        return self._person_id
    
    def set_person_id(self, person_id):
        self._person_id = person_id
    
    def get_name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name
    
    def get_email(self):
        return self._email
    
    def set_email(self, email):
        self._email = email
    
    def get_phone(self):
        return self._phone
    
    def set_phone(self, phone):
        self._phone = phone
    
    def get_is_active(self):
        return self._is_active
    
    def set_is_active(self, is_active):
        self._is_active = is_active
    
    @abstractmethod
    def get_role(self):
        pass
    
    @abstractmethod
    def display_info(self):
        pass
    
    def to_dict(self):
        return {
            'person_id': self._person_id,
            'name': self._name,
            'email': self._email,
            'phone': self._phone,
            'is_active': self._is_active
        }


class Admin(Person):
    def __init__(self, person_id, name, email, phone, admin_level):
        super().__init__(person_id, name, email, phone)
        self._admin_level = admin_level
        self._permissions = ['add_user', 'delete_user', 'add_book', 'delete_book', 'view_reports']
    
    def get_admin_level(self):
        return self._admin_level
    
    def set_admin_level(self, admin_level):
        self._admin_level = admin_level
    
    def get_permissions(self):
        return self._permissions
    
    def add_permission(self, permission):
        if permission not in self._permissions:
            self._permissions.append(permission)
    
    def remove_permission(self, permission):
        if permission in self._permissions:
            self._permissions.remove(permission)
    
    def has_permission(self, permission):
        return permission in self._permissions
    
    def get_role(self):
        return "Admin"
    
    def display_info(self):
        info = f"Admin ID: {self._person_id}\n"
        info += f"Name: {self._name}\n"
        info += f"Email: {self._email}\n"
        info += f"Phone: {self._phone}\n"
        info += f"Admin Level: {self._admin_level}\n"
        info += f"Active: {self._is_active}\n"
        info += f"Permissions: {', '.join(self._permissions)}"
        return info
    
    def to_dict(self):
        data = super().to_dict()
        data['role'] = 'admin'
        data['admin_level'] = self._admin_level
        data['permissions'] = self._permissions
        return data


class Librarian(Person):
    def __init__(self, person_id, name, email, phone, employee_id, shift):
        super().__init__(person_id, name, email, phone)
        self._employee_id = employee_id
        self._shift = shift
        self._books_issued = 0
    
    def get_employee_id(self):
        return self._employee_id
    
    def set_employee_id(self, employee_id):
        self._employee_id = employee_id
    
    def get_shift(self):
        return self._shift
    
    def set_shift(self, shift):
        self._shift = shift
    
    def get_books_issued(self):
        return self._books_issued
    
    def increment_books_issued(self):
        self._books_issued += 1
    
    def reset_books_issued(self):
        self._books_issued = 0
    
    def get_role(self):
        return "Librarian"
    
    def display_info(self):
        info = f"Librarian ID: {self._person_id}\n"
        info += f"Name: {self._name}\n"
        info += f"Email: {self._email}\n"
        info += f"Phone: {self._phone}\n"
        info += f"Employee ID: {self._employee_id}\n"
        info += f"Shift: {self._shift}\n"
        info += f"Books Issued: {self._books_issued}\n"
        info += f"Active: {self._is_active}"
        return info
    
    def to_dict(self):
        data = super().to_dict()
        data['role'] = 'librarian'
        data['employee_id'] = self._employee_id
        data['shift'] = self._shift
        data['books_issued'] = self._books_issued
        return data


class Member(Person):
    def __init__(self, person_id, name, email, phone, membership_date):
        super().__init__(person_id, name, email, phone)
        self._membership_date = membership_date
        self._borrowed_books = []
        self._fine_amount = 0.0
        self._max_books = 5
    
    def get_membership_date(self):
        return self._membership_date
    
    def set_membership_date(self, membership_date):
        self._membership_date = membership_date
    
    def get_borrowed_books(self):
        return self._borrowed_books
    
    def add_borrowed_book(self, book_id):
        if book_id not in self._borrowed_books:
            self._borrowed_books.append(book_id)
    
    def remove_borrowed_book(self, book_id):
        if book_id in self._borrowed_books:
            self._borrowed_books.remove(book_id)
    
    def get_borrowed_books_count(self):
        return len(self._borrowed_books)
    
    def can_borrow_more(self):
        return len(self._borrowed_books) < self._max_books
    
    def get_fine_amount(self):
        return self._fine_amount
    
    def add_fine(self, amount):
        self._fine_amount += amount
    
    def pay_fine(self, amount):
        if amount <= self._fine_amount:
            self._fine_amount -= amount
            return True
        return False
    
    def clear_fine(self):
        self._fine_amount = 0.0
    
    def get_max_books(self):
        return self._max_books
    
    def set_max_books(self, max_books):
        self._max_books = max_books
    
    def get_role(self):
        return "Member"
    
    def display_info(self):
        info = f"Member ID: {self._person_id}\n"
        info += f"Name: {self._name}\n"
        info += f"Email: {self._email}\n"
        info += f"Phone: {self._phone}\n"
        info += f"Membership Date: {self._membership_date}\n"
        info += f"Borrowed Books: {len(self._borrowed_books)}/{self._max_books}\n"
        info += f"Fine Amount: ${self._fine_amount:.2f}\n"
        info += f"Active: {self._is_active}"
        return info
    
    def to_dict(self):
        data = super().to_dict()
        data['role'] = 'member'
        data['membership_date'] = self._membership_date
        data['borrowed_books'] = self._borrowed_books
        data['fine_amount'] = self._fine_amount
        data['max_books'] = self._max_books
        return data