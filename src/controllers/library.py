from datetime import datetime
from models.person import Admin, Librarian, Member
from models.book import Book
from models.transaction import BorrowTransaction, ReturnTransaction
from utils.database import Database
from utils.validator import Validator
from utils.search_engine import SearchEngine
from utils.report_generator import ReportGenerator


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
    
    def get_all_books(self):
        return self._books
    
    def get_book_by_id(self, book_id):
        for book in self._books:
            if book.get_book_id() == book_id:
                return book
        return None
    
    def add_admin(self, name, email, phone, admin_level):
        if not Validator.validate_email(email):
            return False, "Invalid email format"
        if not Validator.validate_phone(phone):
            return False, "Invalid phone format"
        
        admin = Admin(self._next_user_id, name, email, phone, admin_level)
        self._users.append(admin)
        self._next_user_id += 1
        self.save_all_data()
        return True, f"Admin added successfully with ID: {admin.get_person_id()}"
    
    def add_librarian(self, name, email, phone, employee_id, shift):
        if not Validator.validate_email(email):
            return False, "Invalid email format"
        if not Validator.validate_phone(phone):
            return False, "Invalid phone format"
        
        librarian = Librarian(self._next_user_id, name, email, phone, employee_id, shift)
        self._users.append(librarian)
        self._next_user_id += 1
        self.save_all_data()
        return True, f"Librarian added successfully with ID: {librarian.get_person_id()}"
    
    def add_member(self, name, email, phone):
        if not Validator.validate_email(email):
            return False, "Invalid email format"
        if not Validator.validate_phone(phone):
            return False, "Invalid phone format"
        
        membership_date = datetime.now().strftime("%Y-%m-%d")
        member = Member(self._next_user_id, name, email, phone, membership_date)
        self._users.append(member)
        self._next_user_id += 1
        self.save_all_data()
        return True, f"Member added successfully with ID: {member.get_person_id()}"
    
    def remove_user(self, user_id):
        for user in self._users:
            if user.get_person_id() == user_id:
                if isinstance(user, Member) and user.get_borrowed_books_count() > 0:
                    return False, "Cannot remove member with borrowed books"
                self._users.remove(user)
                self.save_all_data()
                return True, "User removed successfully"
        return False, "User not found"
    
    def get_all_users(self):
        return self._users
    
    def get_user_by_id(self, user_id):
        for user in self._users:
            if user.get_person_id() == user_id:
                return user
        return None
    
    def get_all_members(self):
        return [user for user in self._users if isinstance(user, Member)]
    
    def borrow_book(self, book_id, member_id, borrow_period=14):
        book = self.get_book_by_id(book_id)
        if not book:
            return False, "Book not found"
        
        member = self.get_user_by_id(member_id)
        if not member or not isinstance(member, Member):
            return False, "Member not found"
        
        if not member.get_is_active():
            return False, "Member account is inactive"
        
        if not member.can_borrow_more():
            return False, f"Member has reached maximum borrow limit ({member.get_max_books()} books)"
        
        if member.get_fine_amount() > 0:
            return False, f"Member has unpaid fines: ${member.get_fine_amount():.2f}"
        
        if not book.get_is_available():
            return False, "Book is already borrowed"
        
        transaction_date = datetime.now().strftime("%Y-%m-%d")
        transaction = BorrowTransaction(
            self._next_transaction_id,
            book_id,
            member_id,
            transaction_date,
            borrow_period
        )
        
        book.borrow_book(member_id)
        member.add_borrowed_book(book_id)
        self._transactions.append(transaction)
        self._next_transaction_id += 1
        self.save_all_data()
        
        return True, f"Book borrowed successfully. Due date: {transaction.get_due_date()}"
    
    def return_book(self, book_id, member_id):
        book = self.get_book_by_id(book_id)
        if not book:
            return False, "Book not found"
        
        member = self.get_user_by_id(member_id)
        if not member or not isinstance(member, Member):
            return False, "Member not found"
        
        if book.get_is_available():
            return False, "Book is not currently borrowed"
        
        if book.get_borrower_id() != member_id:
            return False, "This book was not borrowed by this member"
        
        borrow_transaction = None
        for trans in self._transactions:
            if (trans.get_book_id() == book_id and 
                trans.get_member_id() == member_id and 
                trans.get_transaction_type() == "borrow" and 
                trans.get_return_date() is None):
                borrow_transaction = trans
                break
        
        if not borrow_transaction:
            return False, "Borrow transaction not found"
        
        return_date = datetime.now().strftime("%Y-%m-%d")
        return_transaction = ReturnTransaction(
            self._next_transaction_id,
            book_id,
            member_id,
            return_date,
            borrow_transaction
        )
        
        fine_amount = return_transaction.get_fine_amount()
        if fine_amount > 0:
            member.add_fine(fine_amount)
        
        borrow_transaction.set_return_date(return_date)
        book.return_book()
        member.remove_borrowed_book(book_id)
        self._transactions.append(return_transaction)
        self._next_transaction_id += 1
        self.save_all_data()
        
        if fine_amount > 0:
            return True, f"Book returned. Fine: ${fine_amount:.2f}"
        return True, "Book returned successfully"
    
    def pay_member_fine(self, member_id, amount):
        member = self.get_user_by_id(member_id)
        if not member or not isinstance(member, Member):
            return False, "Member not found"
        
        if amount <= 0:
            return False, "Invalid payment amount"
        
        if amount > member.get_fine_amount():
            return False, f"Payment amount exceeds fine amount (${member.get_fine_amount():.2f})"
        
        member.pay_fine(amount)
        self.save_all_data()
        remaining = member.get_fine_amount()
        return True, f"Payment successful. Remaining fine: ${remaining:.2f}"
    
    def get_member_borrowed_books(self, member_id):
        member = self.get_user_by_id(member_id)
        if not member or not isinstance(member, Member):
            return []
        
        borrowed_book_ids = member.get_borrowed_books()
        borrowed_books = []
        for book_id in borrowed_book_ids:
            book = self.get_book_by_id(book_id)
            if book:
                borrowed_books.append(book)
        return borrowed_books
    
    def search_books_by_title(self, title):
        return SearchEngine.search_books_by_title(self._books, title)
    
    def search_books_by_author(self, author):
        return SearchEngine.search_books_by_author(self._books, author)
    
    def search_books_by_isbn(self, isbn):
        return SearchEngine.search_books_by_isbn(self._books, isbn)
    
    def search_books_by_category(self, category):
        return SearchEngine.search_books_by_category(self._books, category)
    
    def get_available_books(self):
        return SearchEngine.search_available_books(self._books)
    
    def get_borrowed_books(self):
        return SearchEngine.search_borrowed_books(self._books)
    
    def search_users_by_name(self, name):
        return SearchEngine.search_user_by_name(self._users, name)
    
    def get_members_with_fines(self):
        return SearchEngine.search_members_with_fines(self._users)
    
    def generate_most_borrowed_report(self, top_n=10):
        return ReportGenerator.generate_most_borrowed_books(self._books, top_n)
    
    def generate_active_members_report(self):
        return ReportGenerator.generate_active_members_report(self._users)
    
    def generate_overdue_report(self):
        return ReportGenerator.generate_overdue_books_report(self._transactions, self._books, self._users)
    
    def generate_fine_revenue_report(self):
        return ReportGenerator.generate_fine_revenue_report(self._users)
    
    def generate_category_report(self):
        return ReportGenerator.generate_books_by_category_report(self._books)
    
    def get_all_transactions(self):
        return self._transactions
    
    def get_member_transactions(self, member_id):
        member_transactions = []
        for trans in self._transactions:
            if trans.get_member_id() == member_id:
                member_transactions.append(trans)
        return member_transactions
