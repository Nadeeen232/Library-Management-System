import json
import os


class AuthSystem:
    def __init__(self, credentials_file="library_data/credentials.json"):
        self._credentials_file = credentials_file
        self._current_user = None
        self._current_role = None
        self.ensure_credentials_file()

    def ensure_credentials_file(self):
        if not os.path.exists(self._credentials_file):
            default_credentials = {
                "admin": {
                    "username": "admin",
                    "password": "admin123",
                    "role": "admin",
                    "user_id": 1
                },
                "librarian": {
                    "username": "librarian",
                    "password": "lib123",
                    "role": "librarian",
                    "user_id": 2
                }
            }
            os.makedirs(os.path.dirname(self._credentials_file), exist_ok=True)
            with open(self._credentials_file, 'w') as f:
                json.dump(default_credentials, f, indent=4)
            print(f"Created default credentials file")

    def load_credentials(self):
            try:
                with open(self._credentials_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading credentials: {e}")
                return {}
    def save_credentials(self, credentials):
        try:
            with open(self._credentials_file, 'w') as f:
                json.dump(credentials, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving credentials: {e}")
            return False
    def login(self, username, password):
        credentials = self.load_credentials()
        if username in credentials:
            if credentials[username]["password"] == password:
                self._current_user = username
                self._current_role = credentials[username]["role"]
                print(f"\nLogin successful! Welcome {username} ({self._current_role})")
                return True
        print("\nInvalid username or password!")
        return False
    
    def logout(self):
        self._current_user = None
        self._current_role = None
        print("\nLogged out successfully!")
    
    def is_logged_in(self):
        return self._current_user is not None
    
    def get_current_user(self):
        return self._current_user
    
    def get_current_role(self):
        return self._current_role
    
    def is_admin(self):
        return self._current_role == "admin"
    
    def is_librarian(self):
        return self._current_role == "librarian"
    
    def is_member(self):
        return self._current_role == "member"
    
    def can_manage_users(self):
        return self.is_admin()
    
    def can_manage_books(self):
        return self.is_admin() or self.is_librarian()
    
    def can_manage_transactions(self):
        return self.is_admin() or self.is_librarian()
    
    def can_view_reports(self):
        return self.is_admin() or self.is_librarian()
    
    def add_user_credentials(self, username, password, role, user_id):
        credentials = self.load_credentials()
        if username in credentials:
            return False, "Username already exists"
        credentials[username] = {
            "username": username,
            "password": password,
            "role": role,
            "user_id": user_id
        }
        if self.save_credentials(credentials):
            return True, "User credentials added successfully"
        return False, "Failed to save credentials"
    
    def remove_user_credentials(self, username):
        credentials = self.load_credentials()
        if username not in credentials:
            return False, "Username not found"
        del credentials[username]
        if self.save_credentials(credentials):
            return True, "User credentials removed successfully"
        return False, "Failed to save credentials"