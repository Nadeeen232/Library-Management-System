# ==========================================
# Project: Library Management System
# Module: utils/validator.py
# Purpose: Data Validation & Integrity Checks
# Role: Member 4 - Logic Specialist
# ==========================================

from datetime import datetime
import re # سنستخدمه للتحقق من الإيميل بشكل أدق

class Validator:
    """
    Provides static utility methods to validate various system inputs.
    Ensures data integrity before processing or storage.
    """

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validates email format using basic pattern matching."""
        if not email:
            return False
        # لمسة احترافية: التحقق من وجود @ و . مع التأكد من ترتيبهم
        return '@' in email and '.' in email.split('@')[-1]

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Sanitizes and validates phone numbers (min 10 digits)."""
        # Cleaning the input from common formatting characters
        cleaned = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        return len(cleaned) >= 10 and cleaned.isdigit()

    @staticmethod
    def validate_isbn(isbn: str) -> bool:
        """Validates ISBN-10 or ISBN-13 formats."""
        cleaned = isbn.replace('-', '').replace(' ', '')
        # Check for standard ISBN lengths
        if len(cleaned) in [10, 13] and cleaned.isdigit():
            return True
        return False

    @staticmethod
    def validate_year(year: str) -> bool:
        """Validates that the publication year is realistic."""
        try:
            year_int = int(year)
            current_year = datetime.now().year
            # Logical range: from the first printed book to the current year
            return 1000 <= year_int <= current_year
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_date(date_string: str) -> bool:
        """Validates date format (YYYY-MM-DD)."""
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_non_empty(value: str) -> bool:
        """Ensures the input is not just whitespace."""
        return bool(value and value.strip())
