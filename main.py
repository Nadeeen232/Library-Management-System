# src/main.py
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from controllers.library import Library
from utils.auth import AuthSystem
from views.menu import (
    handle_book_management,
    handle_user_management,
    handle_transactions,
    handle_search,
    handle_reports,
    handle_member_portal, display_book_menu, display_member_menu
)


def display_login_menu():
    print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1. Login")
    print("2. Exit")
    print("=====================================")


def display_main_menu():
    print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1. Book Management")
    print("2. User Management")
    print("3. Transactions")
    print("4. Search")
    print("5. Reports")
    print("6. Logout")
    print("=====================================")


def handle_login(auth_system):
    print("\n--- Login ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    return auth_system.login(username, password)


def main():
    library = Library()
    auth_system = AuthSystem()
    
    print("\n" + "="*60)
    print("WELCOME TO LIBRARY MANAGEMENT SYSTEM")
    print("="*60)
    print("\n🔐 You must log in to access the system")
    print("\nDefault Login Credentials:")
    print("  Admin     - Username: admin     Password: admin123")
    print("  Librarian - Username: librarian Password: lib123")
    print("="*60)
    
    # Login loop - MUST login to continue
    while not auth_system.is_logged_in():
        display_login_menu()
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            if handle_login(auth_system):
                break  # Exit login loop on successful login
        elif choice == "2":
            print("\nGoodbye!")
            return
        else:
            print("Invalid choice. Please try again.")
    
    # Check if member logged in - give them member portal
    if auth_system.is_member():
        display_book_menu()
        handle_member_portal(library, auth_system)
        print("\nThank you for using the Library Management System!")
        return
    
    # Main application loop - for Admin and Librarian only
    while auth_system.is_logged_in():
        display_member_menu()
        print(f"\n👤 Logged in as: {auth_system.get_current_user()} ({auth_system.get_current_role()})")
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            if auth_system.can_manage_books():
                handle_book_management(library)
            else:
                print("\n❌ ACCESS DENIED! Only Admin and Librarian can manage books.")
                input("Press Enter to continue...")
        
        elif choice == "2":
            if auth_system.can_manage_users():
                handle_user_management(library, auth_system)
            else:
                print("\n❌ ACCESS DENIED! Only Admin can manage users.")
                input("Press Enter to continue...")
        
        elif choice == "3":
            if auth_system.can_manage_transactions():
                handle_transactions(library)
            else:
                print("\n❌ ACCESS DENIED! Only Admin and Librarian can manage transactions.")
                input("Press Enter to continue...")
        
        elif choice == "4":
            # Everyone can search
            handle_search(library)
        
        elif choice == "5":
            if auth_system.can_view_reports():
                handle_reports(library)
            else:
                print("\n❌ ACCESS DENIED! Only Admin and Librarian can view reports.")
                input("Press Enter to continue...")
        
        elif choice == "6":
            print("\n🚪 Logging out...")
            auth_system.logout()
            print("\nThank you for using the Library Management System!")
            print("Returning to login screen...\n")
            # Return to login
            main()
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()