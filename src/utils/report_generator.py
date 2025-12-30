# ==========================================
# Project: Library Management System
# Module: utils/report_generator.py
# Purpose: Analytical Reporting & Statistics
# Role: Member 4 - Logic Specialist
# ==========================================

import sys
import os
from typing import List, Dict # لتوثيق أنواع البيانات بشكل احترافي

# Ensure parent directory is accessible
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.person import Member
from utils.search_engine import SearchEngine

class ReportGenerator:
    """
    Utility class dedicated to generating structured reports 
    regarding library assets, user activities, and financial data.
    """

    @staticmethod
    def generate_most_borrowed_books(books: list, top_n: int = 10) -> List:
        """Identifies top performing books based on borrow frequency."""
        # Sorting using a lambda function for efficiency
        return sorted(books, key=lambda x: x.get_total_borrows(), reverse=True)[:top_n]

    @staticmethod
    def generate_active_members_report(users: list) -> str:
        """Generates a formatted summary of all active library members."""
        members = [user for user in users if isinstance(user, Member) and user.get_is_active()]
        
        report = "📊 ACTIVE MEMBERS REPORT\n"
        report += "=" * 30 + "\n"
        report += f"Total Active Count: {len(members)}\n\n"
        
        for member in members:
            report += f"• ID: {member.get_person_id():<5} | Name: {member.get_name():<15} | "
            report += f"Books: {member.get_borrowed_books_count()}\n"
        return report

    @staticmethod
    def generate_overdue_books_report(transactions: list, books: list, users: list) -> str:
        """Consolidates data for all books past their due date."""
        overdue_list = []
        for trans in transactions:
            if trans.get_transaction_type() == "borrow" and trans.is_overdue():
                # Efficiently finding the book object
                book = next((b for b in books if b.get_book_id() == trans.get_book_id()), None)
                member = SearchEngine.search_user_by_id(users, trans.get_member_id())
                
                if book and member:
                    overdue_list.append({
                        'transaction': trans,
                        'book': book,
                        'member': member
                    })
        
        report = "⚠️ OVERDUE BOOKS AUDIT\n"
        report += "=" * 30 + "\n"
        report += f"Total Overdue Items: {len(overdue_list)}\n\n"
        
        for item in overdue_list:
            report += f"Book   : {item['book'].get_title()}\n"
            report += f"Member : {item['member'].get_name()}\n"
            report += f"Delay  : {item['transaction'].get_days_overdue()} Days\n"
            report += f"Due on : {item['transaction'].get_due_date()}\n"
            report += "-" * 20 + "\n"
        return report

    @staticmethod
    def generate_fine_revenue_report(users: list) -> str:
        """Calculates and formats total outstanding fines."""
        total_fines = 0.0
        member_fines = []
        
        for user in users:
            if isinstance(user, Member):
                fine = user.get_fine_amount()
                if fine > 0:
                    member_fines.append({'name': user.get_name(), 'id': user.get_person_id(), 'fine': fine})
                    total_fines += fine
        
        report = "💰 FINANCIAL REPORT: OUTSTANDING FINES\n"
        report += "=" * 40 + "\n"
        report += f"Total Revenue Pending: ${total_fines:.2f}\n"
        report += f"Debtor Count: {len(member_fines)}\n\n"
        
        for item in member_fines:
            report += f"ID: {item['id']:<5} | Name: {item['name']:<15} | Fine: ${item['fine']:.2f}\n"
        return report

    @staticmethod
    def generate_books_by_category_report(books: list) -> str:
        """Provides a statistical breakdown of books per category."""
        categories: Dict[str, int] = {}
        for book in books:
            cat = book.get_category()
            categories[cat] = categories.get(cat, 0) + 1
        
        report = "📂 INVENTORY BY CATEGORY\n"
        report += "=" * 30 + "\n"
        for category, count in sorted(categories.items()):
            report += f"{category:<15}: {count} books\n"
        return report
