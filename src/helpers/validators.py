import re


def validate_swedish_personal_number(personal_number: str) -> bool:
    """
    Validates a Swedish personal number (personnummer).
    A valid personal number has 10 or 12 digits, may include a dash (-),
    and passes the Luhn algorithm (checksum).

    Args:
        personal_number (str): The personal number to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    # Remove dash and spaces for normalization
    sanitized_number = personal_number.replace("-", "").replace(" ", "")

    # Match 10 or 12-digit numbers only
    if not re.fullmatch(r'\d{10}|\d{12}', sanitized_number):
        return False

    # Ensure the number is 10 digits by trimming any leading century digits
    if len(sanitized_number) == 12:
        sanitized_number = sanitized_number[2:]

    # Validate using the Luhn algorithm
    def luhn_checksum(number: str) -> bool:
        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits) + sum(sum(digits_of(d * 2)) for d in even_digits)
        return checksum % 10 == 0

    return luhn_checksum(sanitized_number)
