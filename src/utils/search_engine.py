# ==========================================
# Project: Library Management System
# Module: utils/search_engine.py
# Purpose: High-performance Searching & Filtering
# Role: Member 4 - Logic Specialist
# ==========================================

from typing import List, Optional # لإضافة لمسة احترافية في تعريف الدوال
from models.person import Member

class SearchEngine:
    """
    Advanced Search Engine utility for library assets and user records.
    Provides optimized filtering methods for various data types.
    """

    @staticmethod
    def search_books_by_title(books: list, title: str) -> List:
        """Filters books using a case-insensitive title match."""
        query = title.lower()
        return [book for book in books if query in book.get_title().lower()]

    @staticmethod
    def search_books_by_author(books: list, author: str) -> List:
        """Filters books based on the author's name."""
        query = author.lower()
        return [book for book in books if query in book.get_author().lower()]

    @staticmethod
    def search_books_by_isbn(books: list, isbn: str) -> Optional:
        """Unique search for a book by its ISBN."""
        for book in books:
            if book.get_isbn() == isbn:
                return book
        return None

    @staticmethod
    def search_books_by_category(books: list, category: str) -> List:
        """Returns all books within a specific genre/category."""
        query = category.lower()
        return [book for book in books if query == book.get_category().lower()]

    @staticmethod
    def search_available_books(books: list) -> List:
        """Retrieves all books currently present in the library."""
        return [book for book in books if book.get_is_available()]

    @staticmethod
    def search_borrowed_books(books: list) -> List:
        """Retrieves a list of all books currently on loan."""
        return [book for book in books if not book.get_is_available()]

    @staticmethod
    def search_user_by_id(users: list, user_id: str) -> Optional:
        """Locates a specific user by their unique ID."""
        for user in users:
            if user.get_person_id() == user_id:
                return user
        return None

    @staticmethod
    def search_user_by_name(users: list, name: str) -> List:
        """Filters users by name with partial matching support."""
        query = name.lower()
        return [user for user in users if query in user.get_name().lower()]

    @staticmethod
    def search_members_with_fines(users: list) -> List:
        """Identifies members with outstanding library fines."""
        return [user for user in users if isinstance(user, Member) and user.get_fine_amount() > 0]
