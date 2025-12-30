# Import required classes for handling dates and time differences
from datetime import datetime, timedelta

# Transaction class represents a borrowing or returning operation in the library system
class Transaction:
    def __init__(self, transaction_id, book_id, member_id, transaction_type, transaction_date):
        # Unique ID for the transaction
        self._transaction_id = transaction_id
        # ID of the book involved in the transaction
        self._book_id = book_id
        # ID of the member who performed the transaction
        self._member_id = member_id
        # Type of transaction (e.g., borrow or return)
        self._transaction_type = transaction_type
        # Date when the transaction occurred
        self._transaction_date = transaction_date
        # Due date for returning the book (if applicable)
        self._due_date = None
        # Actual return date of the book
        self._return_date = None
        # Fine amount calculated for late returns
        self._fine_amount = 0.0
    # Getter and setter for transaction ID
    def get_transaction_id(self):
        return self._transaction_id
    
    def set_transaction_id(self, transaction_id):
        self._transaction_id = transaction_id
    # Getter and setter for book ID
    def get_book_id(self):
        return self._book_id
    
    def set_book_id(self, book_id):
        self._book_id = book_id
    # Getter and setter for member ID
    def get_member_id(self):
        return self._member_id
    
    def set_member_id(self, member_id):
        self._member_id = member_id
    # Getter and setter for transaction type
    def get_transaction_type(self):
        return self._transaction_type
    
    def set_transaction_type(self, transaction_type):
        self._transaction_type = transaction_type
    # Getter and setter for transaction date
    def get_transaction_date(self):
        return self._transaction_date
    
    def set_transaction_date(self, transaction_date):
        self._transaction_date = transaction_date
    # Getter and setter for due date
    def get_due_date(self):
        return self._due_date
    
    def set_due_date(self, due_date):
        self._due_date = due_date
    # Getter and setter for return date
    def get_return_date(self):
        return self._return_date
    
    def set_return_date(self, return_date):
        self._return_date = return_date
     # Getter and setter for fine amount
    def get_fine_amount(self):
        return self._fine_amount
    
    def set_fine_amount(self, fine_amount):
        self._fine_amount = fine_amount
    
    def calculate_fine(self, fine_per_day=1.0):
        if self._return_date and self._due_date:
            return_date_obj = datetime.strptime(self._return_date, "%Y-%m-%d")
            due_date_obj = datetime.strptime(self._due_date, "%Y-%m-%d")
            if return_date_obj > due_date_obj:
                days_late = (return_date_obj - due_date_obj).days
                self._fine_amount = days_late * fine_per_day
                return self._fine_amount
        return 0.0
    
    def is_overdue(self):
        if self._due_date and not self._return_date:
            due_date_obj = datetime.strptime(self._due_date, "%Y-%m-%d")
            today = datetime.now()
            return today > due_date_obj
        return False
    
    def get_days_overdue(self):
        if self.is_overdue():
            due_date_obj = datetime.strptime(self._due_date, "%Y-%m-%d")
            today = datetime.now()
            return (today - due_date_obj).days
        return 0
    
    def display_info(self):
        info = f"Transaction ID: {self._transaction_id}\n"
        info += f"Book ID: {self._book_id}\n"
        info += f"Member ID: {self._member_id}\n"
        info += f"Type: {self._transaction_type}\n"
        info += f"Transaction Date: {self._transaction_date}\n"
        if self._due_date:
            info += f"Due Date: {self._due_date}\n"
        if self._return_date:
            info += f"Return Date: {self._return_date}\n"
        if self._fine_amount > 0:
            info += f"Fine Amount: ${self._fine_amount:.2f}"
        return info
    
    def to_dict(self):
        return {
            'transaction_id': self._transaction_id,
            'book_id': self._book_id,
            'member_id': self._member_id,
            'transaction_type': self._transaction_type,
            'transaction_date': self._transaction_date,
            'due_date': self._due_date,
            'return_date': self._return_date,
            'fine_amount': self._fine_amount
        }


class BorrowTransaction(Transaction):
    def __init__(self, transaction_id, book_id, member_id, transaction_date, borrow_period=14):
        super().__init__(transaction_id, book_id, member_id, "borrow", transaction_date)
        self._borrow_period = borrow_period
        self.calculate_due_date()
    
    def get_borrow_period(self):
        return self._borrow_period
    
    def set_borrow_period(self, borrow_period):
        self._borrow_period = borrow_period
        self.calculate_due_date()
    
    def calculate_due_date(self):
        transaction_date_obj = datetime.strptime(self._transaction_date, "%Y-%m-%d")
        due_date_obj = transaction_date_obj + timedelta(days=self._borrow_period)
        self._due_date = due_date_obj.strftime("%Y-%m-%d")
    
    def extend_borrow_period(self, additional_days):
        self._borrow_period += additional_days
        self.calculate_due_date()
    
    def display_info(self):
        info = super().display_info()
        info += f"\nBorrow Period: {self._borrow_period} days"
        return info
    
    def to_dict(self):
        data = super().to_dict()
        data['borrow_period'] = self._borrow_period
        return data


class ReturnTransaction(Transaction):
    def __init__(self, transaction_id, book_id, member_id, transaction_date, borrow_transaction):
        super().__init__(transaction_id, book_id, member_id, "return", transaction_date)
        self._return_date = transaction_date
        self._due_date = borrow_transaction.get_due_date()
        self._borrow_transaction_id = borrow_transaction.get_transaction_id()
        self.calculate_fine()
    
    def get_borrow_transaction_id(self):
        return self._borrow_transaction_id
    
    def set_borrow_transaction_id(self, borrow_transaction_id):
        self._borrow_transaction_id = borrow_transaction_id
    
    def display_info(self):
        info = super().display_info()
        info += f"\nBorrow Transaction ID: {self._borrow_transaction_id}"
        return info
    
    def to_dict(self):
        data = super().to_dict()
        data['borrow_transaction_id'] = self._borrow_transaction_id

        return data
