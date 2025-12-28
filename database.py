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