def validate_non_empty_string(value, field_name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def validate_positive_int(value, field_name):
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer")


def validate_isbn(isbn):
    validate_non_empty_string(isbn, "ISBN")
    if len(isbn) < 5:
        raise ValueError("ISBN is too short")
