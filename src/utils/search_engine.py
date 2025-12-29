from models.person import Member


class SearchEngine:
    @staticmethod
    def search_books_by_title(books, title):
        results = []
        title_lower = title.lower()
        for book in books:
            if title_lower in book.get_title().lower():
                results.append(book)
        return results
    
    @staticmethod
    def search_books_by_author(books, author):
        results = []
        author_lower = author.lower()
        for book in books:
            if author_lower in book.get_author().lower():
                results.append(book)
        return results
    
    @staticmethod
    def search_books_by_isbn(books, isbn):
        for book in books:
            if book.get_isbn() == isbn:
                return book
        return None
    
    @staticmethod
    def search_books_by_category(books, category):
        results = []
        category_lower = category.lower()
        for book in books:
            if category_lower == book.get_category().lower():
                results.append(book)
        return results
    
    @staticmethod
    def search_available_books(books):
        results = []
        for book in books:
            if book.get_is_available():
                results.append(book)
        return results
    
    @staticmethod
    def search_borrowed_books(books):
        results = []
        for book in books:
            if not book.get_is_available():
                results.append(book)
        return results
    
    @staticmethod
    def search_user_by_id(users, user_id):
        for user in users:
            if user.get_person_id() == user_id:
                return user
        return None
    
    @staticmethod
    def search_user_by_name(users, name):
        results = []
        name_lower = name.lower()
        for user in users:
            if name_lower in user.get_name().lower():
                results.append(user)
        return results
    
    @staticmethod
    def search_members_with_fines(users):
        results = []
        for user in users:
            if isinstance(user, Member) and user.get_fine_amount() > 0:
                results.append(user)
        return results