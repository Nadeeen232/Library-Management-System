

# ==========================================
# Project: Library Management System
# Module: models/__init__.py
# Purpose: Centralized Model Export Hub
# Role: Member 4 - System Architecture & Logic
# ==========================================

"""
This module serves as the central entry point for all data models.
It facilitates clean imports across the application by exposing 
core entities (Person, Book, Transaction) through the package level.
"""

# --- 1. Identity & User Models ---
# Handling inheritance: Person is the base class for Admin, Librarian, and Member
from .person import Person, Admin, Librarian, Member

# --- 2. Resource Models ---
# Core entity representing library assets
from .book import Book

# --- 3. Activity & Logging Models ---
# Managing the lifecycle of a book loan (Borrowing/Returning)
from .transaction import Transaction, BorrowTransaction, ReturnTransaction

# --- 4. Package Encapsulation ---
# Explicitly defining public API for the 'models' package.
# This ensures only relevant classes are exported when using 'from models import *'
__all__ = [
    # User-related exports
    'Person', 'Admin', 'Librarian', 'Member',
    
    # Asset-related exports
    'Book',
    
    # Logic-related exports
    'Transaction', 'BorrowTransaction', 'ReturnTransaction'
]
