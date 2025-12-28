from datetime import datetime



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