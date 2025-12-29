from datetime import datetime


class Validator:
    @staticmethod
    def validate_email(email):
        if '@' in email and '.' in email:
            return True
        return False
    
    @staticmethod
    def validate_phone(phone):
        cleaned = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        if len(cleaned) >= 10 and cleaned.isdigit():
            return True
        return False
    
    @staticmethod
    def validate_isbn(isbn):
        cleaned = isbn.replace('-', '').replace(' ', '')
        if len(cleaned) == 10 or len(cleaned) == 13:
            if cleaned.isdigit():
                return True
        return False
    
    @staticmethod
    def validate_year(year):
        try:
            year_int = int(year)
            current_year = datetime.now().year
            if 1000 <= year_int <= current_year:
                return True
        except ValueError:
            pass
        return False
    
    @staticmethod
    def validate_date(date_string):
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_non_empty(value):
        if value and len(value.strip()) > 0:
            return True
        return False
