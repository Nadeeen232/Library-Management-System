def print_separator():
    print("\n" + "="*60 + "\n")


def display_main_menu():
    print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1. Book Management")
    print("2. User Management")
    print("3. Transactions")
    print("4. Search")
    print("5. Reports")
    print("6. Logout")
    print("=====================================")


def display_book_menu():
    print("\n===== BOOK MANAGEMENT =====")
    print("1. Add Book")
    print("2. Remove Book")
    print("3. Update Book")
    print("4. View All Books")
    print("5. View Available Books")
    print("6. View Borrowed Books")
    print("7. Back to Main Menu")
    print("===========================")


def display_user_menu():
    print("\n===== USER MANAGEMENT =====")
    print("1. Add Admin")
    print("2. Add Librarian")
    print("3. Add Member")
    print("4. Remove User")
    print("5. View All Users")
    print("6. View All Members")
    print("7. View Members with Fines")
    print("8. Back to Main Menu")
    print("===========================")


def display_transaction_menu():
    print("\n===== TRANSACTIONS =====")
    print("1. Borrow Book")
    print("2. Return Book")
    print("3. Pay Fine")
    print("4. View Member's Borrowed Books")
    print("5. View All Transactions")
    print("6. Back to Main Menu")
    print("========================")


def display_search_menu():
    print("\n===== SEARCH =====")
    print("1. Search Books by Title")
    print("2. Search Books by Author")
    print("3. Search Book by ISBN")
    print("4. Search Books by Category")
    print("5. Search Users by Name")
    print("6. Back to Main Menu")
    print("==================")


def display_report_menu():
    print("\n===== REPORTS =====")
    print("1. Most Borrowed Books")
    print("2. Active Members Report")
    print("3. Overdue Books Report")
    print("4. Fine Revenue Report")
    print("5. Books by Category Report")
    print("6. Back to Main Menu")
    print("===================")


def display_member_menu():
    print("\n===== MEMBER PORTAL =====")
    print("1. Search Books")
    print("2. View My Borrowed Books")
    print("3. View My Account Info")
    print("4. View My Fines")
    print("5. Logout")
    print("=========================")


def handle_book_management(library):
    while True:
        display_book_menu()
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            print("\n--- Add Book ---")
            title = input("Enter title: ").strip()
            author = input("Enter author: ").strip()
            isbn = input("Enter ISBN: ").strip()
            category = input("Enter category: ").strip()
            year = input("Enter publication year: ").strip()
            success, message = library.add_book(title, author, isbn, category, year)
            print(message)
        
        elif choice == "2":
            print("\n--- Remove Book ---")
            try:
                book_id = int(input("Enter book ID: ").strip())
                success, message = library.remove_book(book_id)
                print(message)
            except ValueError:
                print("Invalid book ID")
        
        elif choice == "3":
            print("\n--- Update Book ---")
            try:
                book_id = int(input("Enter book ID: ").strip())
                title = input("Enter new title (or press Enter to skip): ").strip()
                author = input("Enter new author (or press Enter to skip): ").strip()
                category = input("Enter new category (or press Enter to skip): ").strip()
                success, message = library.update_book(
                    book_id,
                    title if title else None,
                    author if author else None,
                    category if category else None
                )
                print(message)
            except ValueError:
                print("Invalid book ID")
        
        elif choice == "4":
            print("\n--- All Books ---")
            books = library.get_all_books()
            if books:
                for book in books:
                    print_separator()
                    print(book.display_info())
                print_separator()
            else:
                print("No books in the library")
        
        elif choice == "5":
            print("\n--- Available Books ---")
            books = library.get_available_books()
            if books:
                for book in books:
                    print_separator()
                    print(book.display_info())
                print_separator()
            else:
                print("No available books")
        
        elif choice == "6":
            print("\n--- Borrowed Books ---")
            books = library.get_borrowed_books()
            if books:
                for book in books:
                    print_separator()
                    print(book.display_info())
                print_separator()
            else:
                print("No borrowed books")
        
        elif choice == "7":
            break
        
        else:
            print("Invalid choice")


def handle_user_management(library, auth_system):
    while True:
        display_user_menu()
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            print("\n--- Add Admin ---")
            name = input("Enter name: ").strip()
            email = input("Enter email: ").strip()
            phone = input("Enter phone: ").strip()
            admin_level = input("Enter admin level: ").strip()
            username = input("Enter username for login: ").strip()
            password = input("Enter password: ").strip()
            
            success, message = library.add_admin(name, email, phone, admin_level)
            print(message)
            
            if success:
                user_id = int(message.split("ID: ")[1])
                auth_success, auth_message = auth_system.add_user_credentials(
                    username, password, "admin", user_id
                )
                print(auth_message)
        
        elif choice == "2":
            print("\n--- Add Librarian ---")
            name = input("Enter name: ").strip()
            email = input("Enter email: ").strip()
            phone = input("Enter phone: ").strip()
            employee_id = input("Enter employee ID: ").strip()
            shift = input("Enter shift: ").strip()
            username = input("Enter username for login: ").strip()
            password = input("Enter password: ").strip()
            
            success, message = library.add_librarian(name, email, phone, employee_id, shift)
            print(message)
            
            if success:
                user_id = int(message.split("ID: ")[1])
                auth_success, auth_message = auth_system.add_user_credentials(
                    username, password, "librarian", user_id
                )
                print(auth_message)
        
        elif choice == "3":
            print("\n--- Add Member ---")
            name = input("Enter name: ").strip()
            email = input("Enter email: ").strip()
            phone = input("Enter phone: ").strip()
            username = input("Enter username for login (optional, press Enter to skip): ").strip()
            
            success, message = library.add_member(name, email, phone)
            print(message)
            
            if success and username:
                password = input("Enter password: ").strip()
                user_id = int(message.split("ID: ")[1])
                auth_success, auth_message = auth_system.add_user_credentials(
                    username, password, "member", user_id
                )
                print(auth_message)
        
        elif choice == "4":
            print("\n--- Remove User ---")
            try:
                user_id = int(input("Enter user ID: ").strip())
                username = input("Enter username to remove credentials (optional): ").strip()
                
                success, message = library.remove_user(user_id)
                print(message)
                
                if success and username:
                    auth_success, auth_message = auth_system.remove_user_credentials(username)
                    print(auth_message)
            except ValueError:
                print("Invalid user ID")
        
        elif choice == "5":
            print("\n--- All Users ---")
            users = library.get_all_users()
            if users:
                for user in users:
                    print_separator()
                    print(user.display_info())
                print_separator()
            else:
                print("No users in the system")
        
        elif choice == "6":
            print("\n--- All Members ---")
            members = library.get_all_members()
            if members:
                for member in members:
                    print_separator()
                    print(member.display_info())
                print_separator()
            else:
                print("No members in the system")
        
        elif choice == "7":
            print("\n--- Members with Fines ---")
            members = library.get_members_with_fines()
            if members:
                for member in members:
                    print_separator()
                    print(member.display_info())
                print_separator()
            else:
                print("No members with fines")
        
        elif choice == "8":
            break
        
        else:
            print("Invalid choice")


def handle_transactions(library):
    while True:
        display_transaction_menu()
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            print("\n--- Borrow Book ---")
            try:
                book_id = int(input("Enter book ID: ").strip())
                member_id = int(input("Enter member ID: ").strip())
                period = input("Enter borrow period in days (default 14): ").strip()
                borrow_period = int(period) if period else 14
                success, message = library.borrow_book(book_id, member_id, borrow_period)
                print(message)
            except ValueError:
                print("Invalid input")
        
        elif choice == "2":
            print("\n--- Return Book ---")
            try:
                book_id = int(input("Enter book ID: ").strip())
                member_id = int(input("Enter member ID: ").strip())
                success, message = library.return_book(book_id, member_id)
                print(message)
            except ValueError:
                print("Invalid input")
        
        elif choice == "3":
            print("\n--- Pay Fine ---")
            try:
                member_id = int(input("Enter member ID: ").strip())
                amount = float(input("Enter payment amount: ").strip())
                success, message = library.pay_member_fine(member_id, amount)
                print(message)
            except ValueError:
                print("Invalid input")
        
        elif choice == "4":
            print("\n--- Member's Borrowed Books ---")
            try:
                member_id = int(input("Enter member ID: ").strip())
                books = library.get_member_borrowed_books(member_id)
                if books:
                    for book in books:
                        print_separator()
                        print(book.display_info())
                    print_separator()
                else:
                    print("Member has no borrowed books")
            except ValueError:
                print("Invalid member ID")
        
        elif choice == "5":
            print("\n--- All Transactions ---")
            transactions = library.get_all_transactions()
            if transactions:
                for trans in transactions:
                    print_separator()
                    print(trans.display_info())
                print_separator()
            else:
                print("No transactions")
        
        elif choice == "6":
            break
        
        else:
            print("Invalid choice")


def handle_search(library):
    while True:
        display_search_menu()
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            print("\n--- Search by Title ---")
            title = input("Enter title: ").strip()
            books = library.search_books_by_title(title)
            if books:
                for book in books:
                    print_separator()
                    print(book.display_info())
                print_separator()
            else:
                print("No books found")
        
        elif choice == "2":
            print("\n--- Search by Author ---")
            author = input("Enter author: ").strip()
            books = library.search_books_by_author(author)
            if books:
                for book in books:
                    print_separator()
                    print(book.display_info())
                print_separator()
            else:
                print("No books found")
        
        elif choice == "3":
            print("\n--- Search by ISBN ---")
            isbn = input("Enter ISBN: ").strip()
            book = library.search_books_by_isbn(isbn)
            if book:
                print_separator()
                print(book.display_info())
                print_separator()
            else:
                print("Book not found")
        
        elif choice == "4":
            print("\n--- Search by Category ---")
            category = input("Enter category: ").strip()
            books = library.search_books_by_category(category)
            if books:
                for book in books:
                    print_separator()
                    print(book.display_info())
                print_separator()
            else:
                print("No books found")
        
        elif choice == "5":
            print("\n--- Search Users by Name ---")
            name = input("Enter name: ").strip()
            users = library.search_users_by_name(name)
            if users:
                for user in users:
                    print_separator()
                    print(user.display_info())
                print_separator()
            else:
                print("No users found")
        
        elif choice == "6":
            break
        
        else:
            print("Invalid choice")


def handle_reports(library):
    while True:
        display_report_menu()
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            print("\n--- Most Borrowed Books ---")
            try:
                top_n = input("Enter number of books to display (default 10): ").strip()
                n = int(top_n) if top_n else 10
                books = library.generate_most_borrowed_report(n)
                if books:
                    for i, book in enumerate(books, 1):
                        print(f"\n{i}. {book.get_title()} by {book.get_author()}")
                        print(f"   Borrowed {book.get_total_borrows()} times")
                else:
                    print("No books to display")
            except ValueError:
                print("Invalid input")
        
        elif choice == "2":
            print("\n--- Active Members Report ---")
            report = library.generate_active_members_report()
            print(report)
        
        elif choice == "3":
            print("\n--- Overdue Books Report ---")
            report = library.generate_overdue_report()
            print(report)
        
        elif choice == "4":
            print("\n--- Fine Revenue Report ---")
            report = library.generate_fine_revenue_report()
            print(report)
        
        elif choice == "5":
            print("\n--- Books by Category Report ---")
            report = library.generate_category_report()
            print(report)
        
        elif choice == "6":
            break
        
        else:
            print("Invalid choice")


def handle_member_portal(library, auth_system):
    credentials = auth_system.load_credentials()
    username = auth_system.get_current_user()
    member_id = credentials[username]["user_id"]
    
    member = library.get_user_by_id(member_id)
    if not member:
        print("Error: Member account not found!")
        return
    
    while True:
        display_member_menu()
        print(f"\n👤 Logged in as: {member.get_name()}")
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            handle_member_search(library)
        
        elif choice == "2":
            print("\n--- My Borrowed Books ---")
            books = library.get_member_borrowed_books(member_id)
            if books:
                for book in books:
                    print_separator()
                    print(book.display_info())
                    transactions = library.get_member_transactions(member_id)
                    for trans in transactions:
                        if (trans.get_book_id() == book.get_book_id() and 
                            trans.get_transaction_type() == "borrow" and 
                            trans.get_return_date() is None):
                            print(f"\nDue Date: {trans.get_due_date()}")
                            if trans.is_overdue():
                                print(f"⚠️ OVERDUE by {trans.get_days_overdue()} days!")
                print_separator()
            else:
                print("You have no borrowed books")
            input("\nPress Enter to continue...")
        
        elif choice == "3":
            print("\n--- My Account Information ---")
            print_separator()
            print(member.display_info())
            print_separator()
            input("\nPress Enter to continue...")
        
        elif choice == "4":
            print("\n--- My Fines ---")
            fine = member.get_fine_amount()
            if fine > 0:
                print(f"💰 Outstanding Fine: ${fine:.2f}")
                print("\nPlease contact the librarian to pay your fine.")
            else:
                print("✅ You have no outstanding fines!")
            input("\nPress Enter to continue...")
        
        elif choice == "5":
            break
        
        else:
            print("Invalid choice")


def handle_member_search(library):
    while True:
        print("\n===== SEARCH BOOKS =====")
        print("1. Search by Title")
        print("2. Search by Author")
        print("3. Search by Category")
        print("4. View All Available Books")
        print("5. Back")
        print("========================")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            print("\n--- Search by Title ---")
            title = input("Enter title: ").strip()
            books = library.search_books_by_title(title)
            display_book_results(books)
        
        elif choice == "2":
            print("\n--- Search by Author ---")
            author = input("Enter author: ").strip()
            books = library.search_books_by_author(author)
            display_book_results(books)
        
        elif choice == "3":
            print("\n--- Search by Category ---")
            category = input("Enter category: ").strip()
            books = library.search_books_by_category(category)
            display_book_results(books)
        
        elif choice == "4":
            print("\n--- Available Books ---")
            books = library.get_available_books()
            display_book_results(books)
        
        elif choice == "5":
            break
        
        else:
            print("Invalid choice")


def display_book_results(books):
    if books:
        print(f"\nFound {len(books)} book(s):\n")
        for book in books:
            print_separator()
            print(f"Book ID: {book.get_book_id()}")
            print(f"Title: {book.get_title()}")
            print(f"Author: {book.get_author()}")
            print(f"Category: {book.get_category()}")
            print(f"ISBN: {book.get_isbn()}")
            print(f"Available: {'Yes ✅' if book.get_is_available() else 'No ❌'}")
        print_separator()
        print("\nTo borrow a book, please contact the librarian with the Book ID.")
    else:
        print("\nNo books found")
    input("\nPress Enter to continue...")