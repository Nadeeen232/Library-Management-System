from abc import ABC, abstractmethod


class StorageBase(ABC):
    @abstractmethod
    def save_books(self, books):
        pass

    @abstractmethod
    def load_books(self):
        pass

    @abstractmethod
    def save_users(self, users):
        pass

    @abstractmethod
    def load_users(self):
        pass

    @abstractmethod
    def save_loans(self, loans):
        pass

    @abstractmethod
    def load_loans(self):
        pass
