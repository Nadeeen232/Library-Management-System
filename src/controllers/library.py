from datetime import datetime
from utils.validator import Validator
from utils.search_engine import SearchEngine


class Library:
    def __init__(self):
        self._books = []
        self._users = []
        self._transactions = []
        self._database = Database()
        self._next_book_id = 1
        self._next_user_id = 1
        self._next_transaction_id = 1
        self.load_all_data()
    
    def load_all_data(self):
        self._books = self._database.load_books()
        self._users = self._database.load_users()
        self._transactions = self._database.load_transactions()
        if self._books:
            self._next_book_id = max([b.get_book_id() for b in self._books]) + 1
        if self._users:
            self._next_user_id = max([u.get_person_id() for u in self._users]) + 1
        if self._transactions:
            self._next_transaction_id = max([t.get_transaction_id() for t in self._transactions]) + 1
    
    def save_all_data(self):
        self._database.save_books(self._books)
        self._database.save_users(self._users)
        self._database.save_transactions(self._transactions)


    def get_all_books(self):
        return self._books
    
    def get_all_users(self):
        return self._users
    
    def get_all_transactions(self):
        return self._transactions


    def add_book(self, title, author, isbn, category, publication_year):
        if not Validator.validate_non_empty(title):
            return False, "Title cannot be empty"
        if not Validator.validate_non_empty(author):
            return False, "Author cannot be empty"
        if not Validator.validate_isbn(isbn):
            return False, "Invalid ISBN format"
        if not Validator.validate_year(publication_year):
            return False, "Invalid publication year"
        
        book = Book(self._next_book_id, title, author, isbn, category, publication_year)
        self._books.append(book)
        self._next_book_id += 1
        self.save_all_data()
        return True, f"Book added successfully with ID: {book.get_book_id()}"
    
    def remove_book(self, book_id):
        for book in self._books:
            if book.get_book_id() == book_id:
                if not book.get_is_available():
                    return False, "Cannot remove borrowed book"
                self._books.remove(book)
                self.save_all_data()
                return True, "Book removed successfully"
        return False, "Book not found"
    
    def update_book(self, book_id, title=None, author=None, category=None):
        for book in self._books:
            if book.get_book_id() == book_id:
                if title:
                    book.set_title(title)
                if author:
                    book.set_author(author)
                if category:
                    book.set_category(category)
                self.save_all_data()
                return True, "Book updated successfully"
        return False, "Book not found"

    def get_book_by_id(self, book_id):
        for book in self._books:
            if book.get_book_id() == book_id:
                return book
        return None
        


