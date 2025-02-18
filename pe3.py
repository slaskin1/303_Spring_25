import string
import datetime

# Function to encode text using Caesar cipher
def encode(input_text: str, shift: int):
    alphabet_lower = string.ascii_lowercase
    alphabet_upper = string.ascii_uppercase
    encoded_text = ""

    for char in input_text:
        if char in alphabet_lower:
            new_char = alphabet_lower[(alphabet_lower.index(char) + shift) % 26]
            encoded_text += new_char
        elif char in alphabet_upper:
            new_char = alphabet_upper[(alphabet_upper.index(char) + shift) % 26]
            encoded_text += new_char
        else:
            encoded_text += char  # Preserve punctuation, spaces, and numbers

    return (list(alphabet_lower), encoded_text)

# Function to decode text using Caesar cipher
def decode(input_text: str, shift: int):
    return encode(input_text, -shift)[1]

# BankAccount class
class BankAccount:
    def __init__(self, name="Rainy", ID="1234", creation_date=None, balance=0):
        self.name = name
        self.ID = ID
        self.creation_date = creation_date if creation_date else datetime.date.today()
        self.balance = balance

        if self.creation_date > datetime.date.today():
            raise Exception("Creation date cannot be in the future.")

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        print(f"Deposited ${amount}. New balance: ${self.balance}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        print(f"Withdrew ${amount}. New balance: ${self.balance}")

    def view_balance(self):
        print(f"Account balance: ${self.balance}")
        return self.balance

# SavingsAccount class
class SavingsAccount(BankAccount):
    def __init__(self, name="Rainy", ID="1234", creation_date=None, balance=0):
        super().__init__(name, ID, creation_date, balance)

    def withdraw(self, amount):
        days_active = (datetime.date.today() - self.creation_date).days
        if days_active < 180:
            raise Exception("Withdrawals are only permitted after 180 days.")
        if amount > self.balance:
            raise Exception("Overdrafts are not permitted.")
        super().withdraw(amount)

# CheckingAccount class
class CheckingAccount(BankAccount):
    def __init__(self, name="Rainy", ID="1234", creation_date=None, balance=0):
        super().__init__(name, ID, creation_date, balance)

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            self.balance -= (amount + 30)  # Apply overdraft fee
            print(f"Overdraft! Withdrawn ${amount}. Fee applied. New balance: ${self.balance}")
        else:
            super().withdraw(amount)

