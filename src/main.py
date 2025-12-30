# ==========================================
# Project: Library Management System
# Module: main.py (Entry Point)
# Role: Member 4 - Logic & System Integration
# ==========================================

import sys
import os

# Ensuring the 'src' directory is in the system path for seamless imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Importing core controllers and utility systems
from controllers.library import Library
from utils.auth import AuthSystem
from views.menu import (
    handle_book_management,
    handle_user_management,
    handle_transactions,
    handle_search,
    handle_reports,
    handle_member_portal
)

def display_login_menu():
    """Renders the initial access gate for users"""
    print("\n" + "◈"*30)
    print("  GATEWAY: LIBRARY SYSTEM  ")
    print("◈"*30)
    print(" [1] Secure Login")
    print(" [2] Exit System")
    print("." + "_"*28 + ".")

def display_main_menu():
    """Renders the primary dashboard for authorized staff"""
    print("\n" + "═"*35)
    print("   ADMINISTRATIVE DASHBOARD   ")
    print("═"*35)
    print(" 1. 📚 Books Catalog")
    print(" 2. 👥 User Accounts")
    print(" 3. 💸 Transactions Log")
    print(" 4. 🔍 Global Search")
    print(" 5. 📊 Analytics & Reports")
    print(" 6. 🚪 Terminate Session")
    print("═"*35)

def handle_login(auth_system):
    """Processes user credentials through the AuthSystem"""
    print("\n--- Identity Verification ---")
    username = input("Enter Username: ").strip()
    password = input("Enter Password: ").strip()
    return auth_system.login(username, password)

def main():
    # Initializing core system components
    library = Library()
    auth_system = AuthSystem()
    
    print("\n" + "★ "*30)
    print("       WELCOME TO THE ADVANCED LIBRARY SYSTEM       ")
    print("★ "*30)
    
    print("\nℹ️  Notice: Authentication is required for full access.")
    print("-" * 45)
    print("🔑 System Default Keys:")
    print("  • Admin:     user(admin)     pass(admin123)")
    print("  • Librarian: user(librarian) pass(lib123)")
    print("-" * 45)
    
    # Member 4 Note: Secure Authentication Loop
    while not auth_system.is_logged_in():
        display_login_menu()
        choice = input("Select Action: ").strip()
        
        if choice == "1":
            if handle_login(auth_system):
                print("\n✅ Access Granted. Welcome back!")
                break
        elif choice == "2":
            print("\nShutting down system... Goodbye!")
            return
        else:
            print("⚠️ Invalid entry. Please choose 1 or 2.")
    
    # Directing Members to their specific portal
    if auth_system.is_member():
        print(f"\n🎯 Welcome, {auth_system.get_current_user()}!")
        handle_member_portal(library, auth_system)
        print("\nSession ended. Thank you!")
        return
    
    # Core Loop for Staff (Admin/Librarian)
    while auth_system.is_logged_in():
        display_main_menu()
        print(f"\n👤 Session: {auth_system.get_current_user()} | Role: {auth_system.get_current_role()}")
        
        choice = input("\nAction Required > ").strip()
        
        # Mapping menu choices to controller handlers
        if choice == "1":
            if auth_system.can_manage_books():
                handle_book_management(library)
            else:
                print("\n🚫 Permission Denied: Staff clearance required.")
                input("Press Enter...")
        
        elif choice == "2":
            if auth_system.can_manage_users():
                handle_user_management(library, auth_system)
            else:
                print("\n🚫 Permission Denied: Admin clearance required.")
                input("Press Enter...")
        
        elif choice == "3":
            if auth_system.can_manage_transactions():
                handle_transactions(library)
            else:
                print("\n🚫 Permission Denied: Staff clearance required.")
                input("Press Enter...")
        
        elif choice == "4":
            # Accessible to all logged-in users
            handle_search(library)
        
        elif choice == "5":
            if auth_system.can_view_reports():
                handle_reports(library)
            else:
                print("\n🚫 Permission Denied: Reports are restricted.")
                input("Press Enter...")
        
        elif choice == "6":
            print("\n🔄 Closing session safely...")
            auth_system.logout()
            print("Successfully logged out.\n")
            main() # Restarting to login screen
            break
        
        else:
            print("⚠️ Unknown command. Please try again.")

if __name__ == "__main__":
    # Starting the application
    main()
