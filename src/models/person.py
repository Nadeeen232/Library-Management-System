from abc import ABC, abstractmethod


class Person(ABC):
    def __init__(self, person_id, name, email, phone):
        self.__person_id = person_id
        self.__name = name
        self.__email = email
        self.__phone = phone
        self.__is_active = True
    
    def get_person_id(self):
        return self.__person_id
    
    def set_person_id(self, person_id):
        self.__person_id = person_id
    
    def get_name(self):
        return self.__name
    
    def set_name(self, name):
        self.__name = name
    
    def get_email(self):
        return self.__email
    
    def set_email(self, email):
        self.__email = email
    
    def get_phone(self):
        return self.__phone
    
    def set_phone(self, phone):
        self.__phone = phone
    
    def get_is_active(self):
        return self.__is_active
    
    def set_is_active(self, is_active):
        self.__is_active = is_active
    
    @abstractmethod
    def get_role(self):
        pass
    
    @abstractmethod
    def display_info(self):
        pass
    
    def to_dict(self):
        return {
            'person_id': self.__person_id,
            'name': self.__name,
            'email': self.__email,
            'phone': self.__phone,
            'is_active': self.__is_active
        }


class Admin(Person):
    def __init__(self, person_id, name, email, phone, admin_level):
        super().__init__(person_id, name, email, phone)
        self.__admin_level = admin_level
        self.__permissions = ['add_user', 'delete_user', 'add_book', 'delete_book', 'view_reports']
    
    def get_admin_level(self):
        return self.__admin_level
    
    def set_admin_level(self, admin_level):
        self.__admin_level = admin_level
    
    def get_permissions(self):
        return self.__permissions
    
    def add_permission(self, permission):
        if permission not in self.__permissions:
            self.__permissions.append(permission)
    
    def remove_permission(self, permission):
        if permission in self.__permissions:
            self.__permissions.remove(permission)
    
    def has_permission(self, permission):
        return permission in self.__permissions
    
    def get_role(self):
        return "Admin"
    
    def display_info(self):
        info = f"Admin ID: {self.__person_id}\n"
        info += f"Name: {self.__name}\n"
        info += f"Email: {self.__email}\n"
        info += f"Phone: {self.__phone}\n"
        info += f"Admin Level: {self.__admin_level}\n"
        info += f"Active: {self.__is_active}\n"
        info += f"Permissions: {', '.join(self.__permissions)}"
        return info
    
    def to_dict(self):
        data = super().to_dict()
        data['role'] = 'admin'
        data['admin_level'] = self.__admin_level
        data['permissions'] = self.__permissions
        return data


class Librarian(Person):
    def __init__(self, person_id, name, email, phone, employee_id, shift):
        super().__init__(person_id, name, email, phone)
        self.__employee_id = employee_id
        self.__shift = shift
        self.__books_issued = 0
    
    def get_employee_id(self):
        return self.__employee_id
    
    def set_employee_id(self, employee_id):
        self.__employee_id = employee_id
    
    def get_shift(self):
        return self.__shift
    
    def set_shift(self, shift):
        self.__shift = shift
    
    def get_books_issued(self):
        return self.__books_issued
    
    def increment_books_issued(self):
        self.__books_issued += 1
    
    def reset_books_issued(self):
        self.__books_issued = 0
    
    def get_role(self):
        return "Librarian"
    
    def display_info(self):
        info = f"Librarian ID: {self.__person_id}\n"
        info += f"Name: {self.__name}\n"
        info += f"Email: {self.__email}\n"
        info += f"Phone: {self.__phone}\n"
        info += f"Employee ID: {self.__employee_id}\n"
        info += f"Shift: {self.__shift}\n"
        info += f"Books Issued: {self.__books_issued}\n"
        info += f"Active: {self.__is_active}"
        return info
    
    def to_dict(self):
        data = super().to_dict()
        data['role'] = 'librarian'
        data['employee_id'] = self.__employee_id
        data['shift'] = self.__shift
        data['books_issued'] = self.__books_issued
        return data


class Member(Person):
    def __init__(self, person_id, name, email, phone, membership_date):
        super().__init__(person_id, name, email, phone)
        self.__membership_date = membership_date
        self.__borrowed_books = []
        self.__fine_amount = 0.0
        self.__max_books = 5
    
    def get_membership_date(self):
        return self.__membership_date
    
    def set_membership_date(self, membership_date):
        self.__membership_date = membership_date
    
    def get_borrowed_books(self):
        return self.__borrowed_books
    
    def add_borrowed_book(self, book_id):
        if book_id not in self.__borrowed_books:
            self.__borrowed_books.append(book_id)
    
    def remove_borrowed_book(self, book_id):
        if book_id in self.__borrowed_books:
            self.__borrowed_books.remove(book_id)
    
    def get_borrowed_books_count(self):
        return len(self.__borrowed_books)
    
    def can_borrow_more(self):
        return len(self.__borrowed_books) < self.__max_books
    
    def get_fine_amount(self):
        return self.__fine_amount
    
    def add_fine(self, amount):
        self.__fine_amount += amount
    
    def pay_fine(self, amount):
        if amount <= self.__fine_amount:
            self.__fine_amount -= amount
            return True
        return False
    
    def clear_fine(self):
        self.__fine_amount = 0.0
    
    def get_max_books(self):
        return self.__max_books
    
    def set_max_books(self, max_books):
        self.__max_books = max_books
    
    def get_role(self):
        return "Member"
    
    def display_info(self):
        info = f"Member ID: {self.__person_id}\n"
        info += f"Name: {self.__name}\n"
        info += f"Email: {self.__email}\n"
        info += f"Phone: {self.__phone}\n"
        info += f"Membership Date: {self.__membership_date}\n"
        info += f"Borrowed Books: {len(self.__borrowed_books)}/{self.__max_books}\n"
        info += f"Fine Amount: ${self.__fine_amount:.2f}\n"
        info += f"Active: {self.__is_active}"
        return info
    
    def to_dict(self):
        data = super().to_dict()
        data['role'] = 'member'
        data['membership_date'] = self.__membership_date
        data['borrowed_books'] = self.__borrowed_books
        data['fine_amount'] = self.__fine_amount
        data['max_books'] = self.__max_books

        return data
