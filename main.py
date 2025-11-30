# ----------------------------------------------------
# 1. MOCK MANAGER CLASS (Placeholder for Team's OOP Logic)
# ----------------------------------------------------
class MockLibraryManager:
    """
    A placeholder class simulating the core OOP logic built by the team.
    This allows the CLI interface to be tested independently.
    """
    def _init_(self):
        print(">> [System]: Initializing Library and loading data...")

    def add_book_interface(self, title, author, isbn):
        """Simulates adding an item to the library system."""
        # This method will be replaced by the actual call to the core logic
        print(f"✅ Request received for adding Item: '{title}' by {author} (ISBN: {isbn})")
        print(">> Delegating to core OOP logic...")

    def register_user_interface(self, user_name, user_id, user_type):
        """Simulates user registration based on type."""
        # This method will be replaced by the actual call to the core logic
        print(f"✅ Request received to register {user_type}: {user_name} (ID: {user_id})")
        print(">> Core logic will handle user object creation and saving.")

    def check_out_interface(self, item_id, user_id):
        """Simulates a checkout transaction."""
        # This method will be replaced by the actual call to the core logic
        print(f"✅ Request received to check out Item {item_id} by User {user_id}")
        print(">> Core logic will handle validation.")

    def return_interface(self, item_id, user_id):
        """Simulates a return transaction."""
        # This method will be replaced by the actual call to the core logic
        print(f"✅ Request received to return Item {item_id} by User {user_id}")
        print(">> Core logic will calculate fines and update status.")

    def show_reports(self, report_choice):
        """Simulates generating a report."""
        print(f"✅ Report request #{report_choice} is being processed...")

    def save_and_exit(self):
        """Saves data before program termination."""
        print("💾 Saving all data and shutting down system...")

# ----------------------------------------------------
# 2. HELPER FUNCTIONS (For better UX and clean code)
# ----------------------------------------------------
def get_valid_input(prompt_message):
    """Gets input from the user with clean formatting."""
    # .strip() removes extra spaces
    return input(f"\n>> {prompt_message}: ").strip()

# ----------------------------------------------------
# 3. THE CLI INTERFACE CLASS (Your core responsibility)
# ----------------------------------------------------
class LibraryCLI:
    """
    The main class managing the Command Line Interface interaction.
    It delegates user commands to the LibraryManager.
    """
    def __init__(self):
        # IMPORTANT: Change this to 'self.library_manager = LibraryManager()' 
        # when the team's code is ready.
        self.library_manager = MockLibraryManager()

    def display_menu(self):
        """Prints the main menu to the console."""
        print("\n" + "="*50)
        print("         Library Management System (LMS)")
        print("="*50)
        print("1. Add New Item (Book, Magazine, etc.)")
        print("2. Register New User (Student/Faculty)")
        print("3. Check Out Item (Borrow)")
        print("4. Return Item")
        print("5. View Reports")
        print("6. Exit System")
        print("-"*50)
    
    # --- Interface Methods ---

    def handle_add_item(self):
        """Collects input for adding a new item and delegates the task."""
        print("\n--- Add New Item ---")
        title = get_valid_input("Enter Item Title")
        author = get_valid_input("Enter Author Name")
        isbn = get_valid_input("Enter ISBN/ID")
        
        # Delegation to the manager
        self.library_manager.add_book_interface(title, author, isbn)

    def handle_register_user(self):
        """Collects input for user registration and delegates the task."""
        print("\n--- Register New User ---")
        user_name = get_valid_input("Enter User Full Name")
        user_id = get_valid_input("Enter User ID (Unique)")
        
        while True:
            user_type_choice = get_valid_input("Enter User Type (1 for Student, 2 for Faculty)")
            if user_type_choice == '1':
                user_type_str = "Student"
                break
            elif user_type_choice == '2':
                user_type_str = "Faculty"
                break
            else:
                print("⚠ Invalid type. Please enter '1' or '2'.")
        
        # Delegation to the manager
        self.library_manager.register_user_interface(user_name, user_id, user_type_str)

    def handle_check_out(self):
        """Collects input for item checkout and delegates the task."""
        print("\n--- Check Out Item ---")
        item_id = get_valid_input("Enter Item ID")
        user_id = get_valid_input("Enter User ID")
        
        # Delegation to the manager
        self.library_manager.check_out_interface(item_id, user_id)

    def handle_return_item(self):
        """Collects input for item return and delegates the task."""
        print("\n--- Return Item ---")
        item_id = get_valid_input("Enter Item ID to return")
        user_id = get_valid_input("Enter User ID returning the item")
        
        # Delegation to the manager
        self.library_manager.return_interface(item_id, user_id)
        
    def handle_view_reports(self):
        """Collects input for selecting a report and delegates the task."""
        print("\n--- System Reports ---")
        print("1. All Available Items")
        print("2. Current Overdue Items")
        
        report_choice = get_valid_input("Select report type")
        
        # Delegation to the manager
        self.library_manager.show_reports(report_choice)


    def run(self):
        """The main loop that controls the interactive CLI."""
        while True:
            self.display_menu()
            
            # --- Robust Input Handling ---
            choice = input(">> Enter option number: ")
            
            if choice == '1':
                self.handle_add_item()
            elif choice == '2':
                self.handle_register_user()
            elif choice == '3':
                self.handle_check_out()
            elif choice == '4':
                self.handle_return_item()
            elif choice == '5':
                self.handle_view_reports()
            elif choice == '6':
                self.library_manager.save_and_exit()
                break
            else:
                print("⚠ Invalid choice. Please enter a number from 1 to 6.")


# ----------------------------------------------------
# 4. MAIN EXECUTION POINT
# ----------------------------------------------------
if __name__== "__main__":
    app = LibraryCLI()
    app.run()