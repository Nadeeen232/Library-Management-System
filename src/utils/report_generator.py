import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.person import Member
from utils.search_engine import SearchEngine


class ReportGenerator:
    @staticmethod
    def generate_most_borrowed_books(books, top_n=10):
        sorted_books = sorted(books, key=lambda x: x.get_total_borrows(), reverse=True)
        return sorted_books[:top_n]
    
    @staticmethod
    def generate_active_members_report(users):
        members = [user for user in users if isinstance(user, Member) and user.get_is_active()]
        report = f"Total Active Members: {len(members)}\n\n"
        for member in members:
            report += f"ID: {member.get_person_id()} | Name: {member.get_name()} | "
            report += f"Books Borrowed: {member.get_borrowed_books_count()}\n"
        return report
    
    @staticmethod
    def generate_overdue_books_report(transactions, books, users):
        overdue_list = []
        for trans in transactions:
            if trans.get_transaction_type() == "borrow" and trans.is_overdue():
                book = None
                for b in books:
                    if b.get_book_id() == trans.get_book_id():
                        book = b
                        break
                member = SearchEngine.search_user_by_id(users, trans.get_member_id())
                if book and member:
                    overdue_list.append({
                        'transaction': trans,
                        'book': book,
                        'member': member
                    })
        
        report = f"Overdue Books Report\n"
        report += f"Total Overdue: {len(overdue_list)}\n\n"
        for item in overdue_list:
            report += f"Book: {item['book'].get_title()}\n"
            report += f"Member: {item['member'].get_name()}\n"
            report += f"Days Overdue: {item['transaction'].get_days_overdue()}\n"
            report += f"Due Date: {item['transaction'].get_due_date()}\n\n"
        return report
    
    @staticmethod
    def generate_fine_revenue_report(users):
        total_fines = 0.0
        member_fines = []
        for user in users:
            if isinstance(user, Member):
                fine = user.get_fine_amount()
                if fine > 0:
                    member_fines.append({
                        'name': user.get_name(),
                        'id': user.get_person_id(),
                        'fine': fine
                    })
                    total_fines += fine
        
        report = f"Fine Revenue Report\n"
        report += f"Total Fines: ${total_fines:.2f}\n"
        report += f"Members with Fines: {len(member_fines)}\n\n"
        for item in member_fines:
            report += f"ID: {item['id']} | Name: {item['name']} | Fine: ${item['fine']:.2f}\n"
        return report
    
    @staticmethod
    def generate_books_by_category_report(books):
        categories = {}
        for book in books:
            category = book.get_category()
            if category in categories:
                categories[category] += 1
            else:
                categories[category] = 1
        
        report = "Books by Category Report\n\n"
        for category, count in sorted(categories.items()):
            report += f"{category}: {count} books\n"
        return report