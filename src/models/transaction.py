# Import required classes for handling dates and time differences
from datetime import datetime, timedelta

# Transaction class represents a borrowing or returning operation in the library system
class Transaction:
    def __init__(self, transaction_id, book_id, member_id, transaction_type, transaction_date):
        # Unique ID for the transaction
        self.__transaction_id = transaction_id
        # ID of the book involved in the transaction
        self.__book_id = book_id
        # ID of the member who performed the transaction
        self.__member_id = member_id
        # Type of transaction (e.g., borrow or return)
        self.__transaction_type = transaction_type
        # Date when the transaction occurred
        self.__transaction_date = transaction_date
        # Due date for returning the book (if applicable)
        self.__due_date = None
        # Actual return date of the book
        self.__return_date = None
        # Fine amount calculated for late returns
        self.__fine_amount = 0.0
    # Getter and setter for transaction ID
    def get_transaction_id(self):
        return self.__transaction_id
    
    def set_transaction_id(self, transaction_id):
        self.__transaction_id = transaction_id
    # Getter and setter for book ID
    def get_book_id(self):
        return self.__book_id
    
    def set_book_id(self, book_id):
        self.__book_id = book_id
    # Getter and setter for member ID
    def get_member_id(self):
        return self.__member_id
    
    def set_member_id(self, member_id):
        self.__member_id = member_id
    # Getter and setter for transaction type
    def get_transaction_type(self):
        return self.__transaction_type
    
    def set_transaction_type(self, transaction_type):
        self.__transaction_type = transaction_type
    # Getter and setter for transaction date
    def get_transaction_date(self):
        return self.__transaction_date
    
    def set_transaction_date(self, transaction_date):
        self.__transaction_date = transaction_date
    # Getter and setter for due date
    def get_due_date(self):
        return self.__due_date
    
    def set_due_date(self, due_date):
        self.__due_date = due_date
    # Getter and setter for return date
    def get_return_date(self):
        return self.__return_date
    
    def set_return_date(self, return_date):
        self.__return_date = return_date
     # Getter and setter for fine amount
    def get_fine_amount(self):
        return self.__fine_amount
    
    def set_fine_amount(self, fine_amount):
        self.__fine_amount = fine_amount
    
    def calculate_fine(self, fine_per_day=1.0):
        if self.__return_date and self.__due_date:
            return_date_obj = datetime.strptime(self.__return_date, "%Y-%m-%d")
            due_date_obj = datetime.strptime(self.__due_date, "%Y-%m-%d")
            if return_date_obj > due_date_obj:
                days_late = (return_date_obj - due_date_obj).days
                self.__fine_amount = days_late * fine_per_day
                return self.__fine_amount
        return 0.0
    
    def is_overdue(self):
        if self.__due_date and not self.__return_date:
            due_date_obj = datetime.strptime(self.__due_date, "%Y-%m-%d")
            today = datetime.now()
            return today > due_date_obj
        return False
    
    def get_days_overdue(self):
        if self.is_overdue():
            due_date_obj = datetime.strptime(self.__due_date, "%Y-%m-%d")
            today = datetime.now()
            return (today - due_date_obj).days
        return 0
    
    def display_info(self):
        info = f"Transaction ID: {self.__transaction_id}\n"
        info += f"Book ID: {self.__book_id}\n"
        info += f"Member ID: {self.__member_id}\n"
        info += f"Type: {self.__transaction_type}\n"
        info += f"Transaction Date: {self.__transaction_date}\n"
        if self.__due_date:
            info += f"Due Date: {self.__due_date}\n"
        if self.__return_date:
            info += f"Return Date: {self.__return_date}\n"
        if self.__fine_amount > 0:
            info += f"Fine Amount: ${self.__fine_amount:.2f}"
        return info
    
    def to_dict(self):
        return {
            'transaction_id': self.__transaction_id,
            'book_id': self.__book_id,
            'member_id': self.__member_id,
            'transaction_type': self.__transaction_type,
            'transaction_date': self.__transaction_date,
            'due_date': self.__due_date,
            'return_date': self.__return_date,
            'fine_amount': self.__fine_amount
        }


class BorrowTransaction(Transaction):
    def __init__(self, transaction_id, book_id, member_id, transaction_date, borrow_period=14):
        super().__init__(transaction_id, book_id, member_id, "borrow", transaction_date)
        self.__borrow_period = borrow_period
        self.calculate_due_date()
    
    def get_borrow_period(self):
        return self.__borrow_period
    
    def set_borrow_period(self, borrow_period):
        self.__borrow_period = borrow_period
        self.calculate_due_date()
    
    def calculate_due_date(self):
        transaction_date_obj = datetime.strptime(self.__transaction_date, "%Y-%m-%d")
        due_date_obj = transaction_date_obj + timedelta(days=self.__borrow_period)
        self.__due_date = due_date_obj.strftime("%Y-%m-%d")
    
    def extend_borrow_period(self, additional_days):
        self.__borrow_period += additional_days
        self.calculate_due_date()
    
    def display_info(self):
        info = super().display_info()
        info += f"\nBorrow Period: {self.__borrow_period} days"
        return info
    
    def to_dict(self):
        data = super().to_dict()
        data['borrow_period'] = self.__borrow_period
        return data


class ReturnTransaction(Transaction):
    def __init__(self, transaction_id, book_id, member_id, transaction_date, borrow_transaction):
        super().__init__(transaction_id, book_id, member_id, "return", transaction_date)
        self.__return_date = transaction_date
        self.__due_date = borrow_transaction.get_due_date()
        self.__borrow_transaction_id = borrow_transaction.get_transaction_id()
        self.calculate_fine()
    
    def get_borrow_transaction_id(self):
        return self.__borrow_transaction_id
    
    def set_borrow_transaction_id(self, borrow_transaction_id):
        self.__borrow_transaction_id = borrow_transaction_id
    
    def display_info(self):
        info = super().display_info()
        info += f"\nBorrow Transaction ID: {self.__borrow_transaction_id}"
        return info
    
    def to_dict(self):
        data = super().to_dict()
        data['borrow_transaction_id'] = self.__borrow_transaction_id

        return data

