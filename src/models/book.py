class Book:
    def __init__(self, book_id, title, author, isbn, category, publication_year):
        self._book_id = book_id
        self._title = title
        self._author = author
        self._isbn = isbn
        self._category = category
        self._publication_year = publication_year
        self._is_available = True
        self._borrower_id = None
        self._total_borrows = 0
    
    def get_book_id(self):
        return self._book_id
    
    def set_book_id(self, book_id):
        self._book_id = book_id
    
    def get_title(self):
        return self._title
    
    def set_title(self, title):
        self._title = title
    
    def get_author(self):
        return self._author
    
    def set_author(self, author):
        self._author = author
    
    def get_isbn(self):
        return self._isbn
    
    def set_isbn(self, isbn):
        self._isbn = isbn
    
    def get_category(self):
        return self._category
    
    def set_category(self, category):
        self._category = category
    
    def get_publication_year(self):
        return self._publication_year
    
    def set_publication_year(self, publication_year):
        self._publication_year = publication_year
    
    def get_is_available(self):
        return self._is_available
    
    def set_is_available(self, is_available):
        self._is_available = is_available
    
    def get_borrower_id(self):
        return self._borrower_id
    
    def set_borrower_id(self, borrower_id):
        self._borrower_id = borrower_id
    
    def get_total_borrows(self):
        return self._total_borrows
    
    def increment_total_borrows(self):
        self._total_borrows += 1
    
    def borrow_book(self, member_id):
        if self._is_available:
            self._is_available = False
            self._borrower_id = member_id
            self._total_borrows += 1
            return True
        return False
    
    def return_book(self):
        if not self._is_available:
            self._is_available = True
            self._borrower_id = None
            return True
        return False
    
    def display_info(self):
        info = f"Book ID: {self._book_id}\n"
        info += f"Title: {self._title}\n"
        info += f"Author: {self._author}\n"
        info += f"ISBN: {self._isbn}\n"
        info += f"Category: {self._category}\n"
        info += f"Publication Year: {self._publication_year}\n"
        info += f"Available: {self._is_available}\n"
        info += f"Total Borrows: {self._total_borrows}"
        if not self._is_available:
            info += f"\nBorrowed by: {self._borrower_id}"
        return info
    
    def to_dict(self):
        return {
            'book_id': self._book_id,
            'title': self._title,
            'author': self._author,
            'isbn': self._isbn,
            'category': self._category,
            'publication_year': self._publication_year,
            'is_available': self._is_available,
            'borrower_id': self._borrower_id,
            'total_borrows': self._total_borrows
        }