class Book:
    def __init__(self, book_id, title, author, isbn, category, publication_year):
        self.__book_id = book_id
        self.__title = title
        self.__author = author
        self.__isbn = isbn
        self.__category = category
        self.__publication_year = publication_year
        self.__is_available = True
        self.__borrower_id = None
        self.__total_borrows = 0
    
    def get_book_id(self):
        return self.__book_id
    
    def set_book_id(self, book_id):
        self.__book_id = book_id
    
    def get_title(self):
        return self.__title
    
    def set_title(self, title):
        self.__title = title
    
    def get_author(self):
        return self.__author
    
    def set_author(self, author):
        self.__author = author
    
    def get_isbn(self):
        return self.__isbn
    
    def set_isbn(self, isbn):
        self.__isbn = isbn
    
    def get_category(self):
        return self.__category
    
    def set_category(self, category):
        self.__category = category
    
    def get_publication_year(self):
        return self.__publication_year
    
    def set_publication_year(self, publication_year):
        self.__publication_year = publication_year
    
    def get_is_available(self):
        return self.__is_available
    
    def set_is_available(self, is_available):
        self.__is_available = is_available
    
    def get_borrower_id(self):
        return self.__borrower_id
    
    def set_borrower_id(self, borrower_id):
        self.__borrower_id = borrower_id
    
    def get_total_borrows(self):
        return self.__total_borrows
    
    def increment_total_borrows(self):
        self.__total_borrows += 1
    
    def borrow_book(self, member_id):
        if self.__is_available:
            self.__is_available = False
            self.__borrower_id = member_id
            self.__total_borrows += 1
            return True
        return False
    
    def return_book(self):
        if not self.__is_available:
            self.__is_available = True
            self.__borrower_id = None
            return True
        return False
    
    def display_info(self):
        info = f"Book ID: {self.__book_id}\n"
        info += f"Title: {self.__title}\n"
        info += f"Author: {self.__author}\n"
        info += f"ISBN: {self.__isbn}\n"
        info += f"Category: {self.__category}\n"
        info += f"Publication Year: {self.__publication_year}\n"
        info += f"Available: {self.__is_available}\n"
        info += f"Total Borrows: {self.__total_borrows}"
        if not self.__is_available:
            info += f"\nBorrowed by: {self.__borrower_id}"
        return info
    
    def to_dict(self):
        return {
            'book_id': self.__book_id,
            'title': self.__title,
            'author': self.__author,
            'isbn': self.__isbn,
            'category': self.__category,
            'publication_year': self.__publication_year,
            'is_available': self.__is_available,
            'borrower_id': self.__borrower_id,
            'total_borrows': self.__total_borrows

        }
