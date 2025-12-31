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
    
    def load_all_data(self): #load data from (folder librry_data) in the attributes and increment the id by 1
        self._books = self._database.load_books() #Load books from database(books.json) in the list (self._books = [])
        self._users = self._database.load_users() 
        self._transactions = self._database.load_transactions()
        if self._books:
            self._next_book_id = max([b.get_book_id() for b in self._books]) + 1
        if self._users:
            self._next_user_id = max([u.get_person_id() for u in self._users]) + 1
        if self._transactions:
            self._next_transaction_id = max([t.get_transaction_id() for t in self._transactions]) + 1

    #method 2
    def save_all_data(self):   #It tells the database to save everything (books, users, and transactions) at (library-data)folder.
        self._database.save_books(self._books)
        self._database.save_users(self._users)
        self._database.save_transactions(self._transactions)
    
    def add_book(self, title, author, isbn, category, publication_year):          #adds a new book to the library, but only after validating the input data.
        if not Validator.validate_non_empty(title):    #it's a static method from (validator.py) 
            return False, "Title cannot be empty"
        if not Validator.validate_non_empty(author):
            return False, "Author cannot be empty"
        if not Validator.validate_isbn(isbn):
            return False, "Invalid ISBN format"
        if not Validator.validate_year(publication_year):
            return False, "Invalid publication year"
        
        book = Book(self._next_book_id, title, author, isbn, category, publication_year) #Instantiates a new book 
        self._books.append(book) #add the new book in the list
        self._next_book_id += 1
        self.save_all_data() #call method 2 to save the new book in library data (books.json)
        return True, f"Book added successfully with ID: {book.get_book_id()}"
    
    def remove_book(self, book_id):   #Removes a book only if it exists and only if it is not currently borrowed
        for book in self._books:
            if book.get_book_id() == book_id:
                if not book.get_is_available():
                    return False, "Cannot remove borrowed book"   #if not exist
                self._books.remove(book)  #if exist remove the book
                self.save_all_data() 
                return True, "Book removed successfully"
        return False, "Book not found"
    
    def update_book(self, book_id, title=None, author=None, category=None):             #to update the book informations
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
        return False, "Book not found"                          #if no matching book ID exists
    
    def get_all_books(self):              #Returns all books in the library.
        return self._books
    
    def get_book_by_id(self, book_id):         #Finds and returns one specific book by its ID.
        for book in self._books:
            if book.get_book_id() == book_id:
                return book
        return None
    
    def add_admin(self, name, email, phone, admin_level):      #adds a new admin but only after validating the input data.
        if not Validator.validate_email(email):
            return False, "Invalid email format"
        if not Validator.validate_phone(phone):
            return False, "Invalid phone format"

     #Admin is a subclass from person  
        admin = Admin(self._next_user_id, name, email, phone, admin_level)
        self._users.append(admin)         #Adds admin to the users list
        self._next_user_id += 1
        self.save_all_data()         #Calls Database.save_users() and writes changes to (users.json)
        return True, f"Admin added successfully with ID: {admin.get_person_id()}"
    
    def add_librarian(self, name, email, phone, employee_id, shift):
        if not Validator.validate_email(email):
            return False, "Invalid email format"
        if not Validator.validate_phone(phone):
            return False, "Invalid phone format"
            
    #Librarian is a subclass from person 
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
            
    #Member is a subclass from person 
        membership_date = datetime.now().strftime("%Y-%m-%d")                    #Generate membership date (year-month-day)
        member = Member(self._next_user_id, name, email, phone, membership_date)
        self._users.append(member)
        self._next_user_id += 1
        self.save_all_data()
        return True, f"Member added successfully with ID: {member.get_person_id()}"
    
    def remove_user(self, user_id):
        for user in self._users:
            if user.get_person_id() == user_id:
                if isinstance(user, Member) and user.get_borrowed_books_count() > 0:  #Checks:if the user a Member? and Do they currently have borrowed books?
                    return False, "Cannot remove member with borrowed books"
                self._users.remove(user)
                self.save_all_data()
                return True, "User removed successfully"
        return False, "User not found"
    
    def get_all_users(self):        #Returns all users in the library.
        return self._users
    
    def get_user_by_id(self, user_id):   #Finds one user by ID.
        for user in self._users:              #search about the id in the list
            if user.get_person_id() == user_id:
                return user
        return None
    
    def get_all_members(self):            #Returns only Member users.
        return [user for user in self._users if isinstance(user, Member)]
    
    def borrow_book(self, book_id, member_id, borrow_period=14):
        book = self.get_book_by_id(book_id)      #Returns a Book by using the method that call(get_book_by_id)
        if not book:
            return False, "Book not found"
        
        member = self.get_user_by_id(member_id)        #Returns a member by using the method that call(get_user_by_id)
        if not member or not isinstance(member, Member):   #cheak if exist and if actually a Member
            return False, "Member not found"
        
        if not member.get_is_active():                #Check if member is active
            return False, "Member account is inactive"
        
        if not member.can_borrow_more():            #Check borrow limit (5books)
            return False, f"Member has reached maximum borrow limit ({member.get_max_books()} books)"
        
        if member.get_fine_amount() > 0:        #Check unpaid fines
            return False, f"Member has unpaid fines: ${member.get_fine_amount():.2f}"
        
        if not book.get_is_available()
            return False, "Book is already borrowed"
        
        transaction_date = datetime.now().strftime("%Y-%m-%d")       #write the transaction date
      #BorrowTransaction is a subclass from Transaction  
        transaction = BorrowTransaction(
            self._next_transaction_id,
            book_id,
            member_id,
            transaction_date,
            borrow_period
        )
        
        book.borrow_book(member_id)        #Marks book unavailable & Stores borrower ID
        member.add_borrowed_book(book_id)     #Tracks borrowed books per member
        self._transactions.append(transaction) #add in the list 
        self._next_transaction_id += 1
        self.save_all_data() #save this transaction in the (transaction.json)
        return True, f"Book borrowed successfully. Due date: {transaction.get_due_date()}"
    
    def return_book(self, book_id, member_id):
        book = self.get_book_by_id(book_id)    #Returns a Book by using the method that call(get_book_by_id)
        if not book:
            return False, "Book not found"
        
        member = self.get_user_by_id(member_id)
        if not member or not isinstance(member, Member):          #cheack if a member only Member type can return books
            return False, "Member not found"
        
        if book.get_is_available():                           #if is available, it is not currently borrowed
            return False, "Book is not currently borrowed"
        
        if book.get_borrower_id() != member_id:              #Ensures correct member returns the book
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
       #ReturnTransaction is a subclass from Transaction
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
        
        member.pay_fine(amount)       #Ensures member cannot overpay.
        self.save_all_data()       
        remaining = member.get_fine_amount()
        return True, f"Payment successful. Remaining fine: ${remaining:.2f}"
    
    def get_member_borrowed_books(self, member_id):              #Returns a list of Book objects currently borrowed by a member.
        member = self.get_user_by_id(member_id)
        if not member or not isinstance(member, Member):     #if not member
            return []                                            #return an empty list
        
        borrowed_book_ids = member.get_borrowed_books()
        borrowed_books = []
        for book_id in borrowed_book_ids:
            book = self.get_book_by_id(book_id)
            if book:
                borrowed_books.append(book)
        return borrowed_books

  #These delegate search functionality to SearchEngine, which is a utility class.
    def search_books_by_title(self, title):                                    #Returns books by titles
        return SearchEngine.search_books_by_title(self._books, title)           
    
    def search_books_by_author(self, author) :                                #Returns books by author
        return SearchEngine.search_books_by_author(self._books, author)
    
    def search_books_by_isbn(self, isbn):                                        #Returns books by isbn
        return SearchEngine.search_books_by_isbn(self._books, isbn)
    
    def search_books_by_category(self, category):                                #Returns books by category   
        return SearchEngine.search_books_by_category(self._books, category)
    
    def get_available_books(self):                                                #Returns books currently available
        return SearchEngine.search_available_books(self._books)
    
    def get_borrowed_books(self):                                                 #Returns books currently borrowed
        return SearchEngine.search_borrowed_books(self._books)
    
    def search_users_by_name(self, name):                                         #Returns users with matching names
        return SearchEngine.search_user_by_name(self._users, name)
    
    def get_members_with_fines(self):                                             #Returns members who owe fines
        return SearchEngine.search_members_with_fines(self._users)
    
    def generate_most_borrowed_report(self, top_n=10):                             #Returns the top N most borrowed books
        return ReportGenerator.generate_most_borrowed_books(self._books, top_n)
    
    def generate_active_members_report(self):                                    #Returns members who borrow the most
        return ReportGenerator.generate_active_members_report(self._users)
    
    def generate_overdue_report(self):                                         #Returns books past due date
        return ReportGenerator.generate_overdue_books_report(self._transactions, self._books, self._users)
    
    def generate_fine_revenue_report(self):                                      #Returns total fines collected
        return ReportGenerator.generate_fine_revenue_report(self._users)
    
    def generate_category_report(self):                                            #Returns count of books by category
        return ReportGenerator.generate_books_by_category_report(self._books)
    
    def get_all_transactions(self):                       #Returns all transactions, borrow and return.
        return self._transactions
    
    def get_member_transactions(self, member_id):     #Returns only transactions for a specific member.
        member_transactions = []
        for trans in self._transactions:
            if trans.get_member_id() == member_id:
                member_transactions.append(trans)
        return member_transactions

