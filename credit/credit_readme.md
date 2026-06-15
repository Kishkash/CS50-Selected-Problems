# Credit Card Validator (CS50 Problem Set – Python)

This is an implementation of a credit card number validator, originally completed as part of Harvard’s CS50 Introduction to Computer Science course.

The goal of the assignment is to determine whether a given credit card number is valid using:

- Card type rules (AMEX, Mastercard, Visa)
- Luhn’s Algorithm, an industry standard checksum used to validate card numbers

This version expands on the original procedural CS50 exercise by rewriting the solution in a clean, object oriented Python design.

## Features

- Detects AMEX, Mastercard, and Visa based on number patterns
- Implements Luhn’s Algorithm to verify checksum validity
- Fully object oriented design (`CreditCard` class)
- No external dependencies
- Works with any numeric input provided by the user

## How It Works

### 1. Card Type Detection

The program checks:

- Length of the card number
- Starting digits (prefix rules)

| Card Type | Length | Prefixes |
|------------|--------|----------|
| AMEX | 15 | 34, 37 |
| Mastercard | 16 | 51–55 |
| Visa | 13, 16 | 4 |

### 2. Luhn’s Algorithm

The validator then applies Luhn’s checksum:

- Double every second digit from the right
- Sum all digits (splitting two digit products)
- A valid card ends with a total divisible by 10

If either step fails, the card is marked `INVALID`.

## Usage

Run the script and enter a credit card number when prompted:

```bash
$ python credit_oop.py
Credit card number: 4111111111111111
VISA
```

## Test Numbers

These are industry standard test card numbers (not real cards):

### Visa

```text
4111111111111111
4012888888881881
4222222222222
```

### Mastercard

```text
5555555555554444
5105105105105100
```

### American Express

```text
378282246310005
371449635398431
```

### Invalid Examples

```text
1234567890123456
4111111111111121
9111111111111111
```

## Code Overview

The project centers around a single class:

```python
class CreditCard:
    def __init__(self, number):
        ...

    def validate(self):
        ...

    def _detect_type(self):
        ...

    def _check_luhn(self, card_type):
        ...
```

The `validate()` method orchestrates the full validation process and returns:

- `"AMEX"`
- `"MASTERCARD"`
- `"VISA"`
- `"INVALID"`

## About CS50

This project is based on Problem Set 6 – Credit from Harvard’s CS50 course.

The original assignment is procedural; this repository contains a refactored, object oriented version created as part of my learning journey.
