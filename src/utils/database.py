import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.person import Admin, Librarian, Member
from models.book import Book
from models.transaction import Transaction


class Database:
    def __init__(self, data_folder="library_data"):
        self._data_folder = data_folder
        self._users_file = os.path.join(data_folder, "users.json")
        self._books_file = os.path.join(data_folder, "books.json")
        self._transactions_file = os.path.join(data_folder, "transactions.json")
        self.ensure_data_folder()
    
    def ensure_data_folder(self):
        if not os.path.exists(self._data_folder):
            os.makedirs(self._data_folder)

            print(f"Created data folder: {self._data_folder}")
    def save_users(self, users):
        try:
            with open(self._users_file, 'w') as f:
                json.dump([user.to_dict() for user in users], f, indent=4)
            print(f"Saved {len(users)} users to {self._users_file}")
            return True
        except Exception as e:
            print(f"Error saving users: {e}")
            return False
    
    def load_users(self):
        try:
            if os.path.exists(self._users_file):
                with open(self._users_file, 'r') as f:
                    data = json.load(f)
                    users = []
                    for user_data in data:
                        if user_data['role'] == 'admin':
                            user = Admin(
                                user_data['person_id'],
                                user_data['name'],
                                user_data['email'],
                                user_data['phone'],
                                user_data['admin_level']
                            )
                        elif user_data['role'] == 'librarian':
                            user = Librarian(
                                user_data['person_id'],
                                user_data['name'],
                                user_data['email'],
                                user_data['phone'],
                                user_data['employee_id'],
                                user_data['shift']
                            )
                        elif user_data['role'] == 'member':
                            user = Member(
                                user_data['person_id'],
                                user_data['name'],
                                user_data['email'],
                                user_data['phone'],
                                user_data['membership_date']
                            )
                            user._borrowed_books = user_data.get('borrowed_books', [])
                            user._fine_amount = user_data.get('fine_amount', 0.0)
                        else:
                            continue
                        user.set_is_active(user_data.get('is_active', True))
                        users.append(user)
                    print(f"Loaded {len(users)} users from {self._users_file}")
                    return users
            else:
                print(f"No users file found at {self._users_file}")
            return []
        except Exception as e:
            print(f"Error loading users: {e}")
            import traceback
            traceback.print_exc()
            return []
    def save_books(self, books):
        try:
            with open(self._books_file, 'w') as f:
                json.dump([book.to_dict() for book in books], f, indent=4)
            print(f"Saved {len(books)} books to {self._books_file}")
            return True
        except Exception as e:
            print(f"Error saving books: {e}")
            return False
    
    def load_books(self):
        try:
            if os.path.exists(self._books_file):
                with open(self._books_file, 'r') as f:
                    data = json.load(f)
                    books = []
                    for book_data in data:
                        book = Book(
                            book_data['book_id'],
                            book_data['title'],
                            book_data['author'],
                            book_data['isbn'],
                            book_data['category'],
                            book_data['publication_year']
                        )
                        book.set_is_available(book_data.get('is_available', True))
                        book.set_borrower_id(book_data.get('borrower_id'))
                        book._total_borrows = book_data.get('total_borrows', 0)
                        books.append(book)
                    print(f"Loaded {len(books)} books from {self._books_file}")
                    return books
            else:
                print(f"No books file found at {self._books_file}")
            return []
        except Exception as e:
            print(f"Error loading books: {e}")
            import traceback
            traceback.print_exc()
            return []
    def save_transactions(self, transactions):
        try:
            with open(self._transactions_file, 'w') as f:
                json.dump([trans.to_dict() for trans in transactions], f, indent=4)
            print(f"Saved {len(transactions)} transactions to {self._transactions_file}")
            return True
        except Exception as e:
            print(f"Error saving transactions: {e}")
            return False
    
    def load_transactions(self):
        try:
            if os.path.exists(self._transactions_file):
                with open(self._transactions_file, 'r') as f:
                    data = json.load(f)
                    transactions = []
                    for trans_data in data:
                        trans = Transaction(
                            trans_data['transaction_id'],
                            trans_data['book_id'],
                            trans_data['member_id'],
                            trans_data['transaction_type'],
                            trans_data['transaction_date']
                        )
                        trans.set_due_date(trans_data.get('due_date'))
                        trans.set_return_date(trans_data.get('return_date'))
                        trans.set_fine_amount(trans_data.get('fine_amount', 0.0))
                        transactions.append(trans)
                    print(f"Loaded {len(transactions)} transactions from {self._transactions_file}")
                    return transactions
            else:
                print(f"No transactions file found at {self._transactions_file}")
            return []
        except Exception as e:
            print(f"Error loading transactions: {e}")
            import traceback
            traceback.print_exc()
            return []

