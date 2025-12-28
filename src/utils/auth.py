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