class CreditCard:
    """Represents a credit card and provides validation utilities."""

    def __init__(self, number: str):
        self.number = number
        self.length = len(number)
        self.type = "INVALID"

    # Public API
    def validate(self):
        """Runs all validation steps and returns the card type."""
        self.type = self._detect_type()
        self.type = self._check_luhn(self.type)
        return self.type

    # Internal helpers
    def _detect_type(self):
        """Return AMEX, MASTERCARD, VISA, or INVALID based on number pattern."""
        first_digit = int(self.number[0])
        first_two = int(self.number[:2])

        if self.length == 15 and first_two in (34, 37):
            return "AMEX"
        elif self.length == 16 and 51 <= first_two <= 55:
            return "MASTERCARD"
        elif self.length in (13, 16) and first_digit == 4:
            return "VISA"
        else:
            return "INVALID"

    def _check_luhn(self, card_type):
        """Validate card number using Luhn's algorithm."""
        if card_type == "INVALID":
            return "INVALID"

        total = 0

        # Double every second digit from the right
        for i in range(self.length - 2, -1, -2):
            doubled = int(self.number[i]) * 2
            total += doubled if doubled < 10 else (doubled // 10 + doubled % 10)

        # Add the remaining digits
        for i in range(self.length - 1, -1, -2):
            total += int(self.number[i])

        return card_type if total % 10 == 0 else "INVALID"


# Program entry point

card_number = input("Credit card number: ")
card = CreditCard(card_number)
print(card.validate())
