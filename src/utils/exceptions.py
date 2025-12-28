class LibraryError(Exception):
    """Base exception for library system"""
    pass


class BookNotFoundError(LibraryError):
    pass


class UserNotFoundError(LibraryError):
    pass


class BookNotAvailableError(LibraryError):
    pass


class MaxBorrowLimitReachedError(LibraryError):
    pass


class LoanNotFoundError(LibraryError):
    pass


class StorageError(LibraryError):
    pass
