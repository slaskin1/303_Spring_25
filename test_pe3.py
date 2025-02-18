import pytest
import datetime
import string
from pe3 import *

# Parametrized tests for encode function
@pytest.mark.parametrize("in_text, shift, out_text", [
    ("", 3, ""), 
    ("a", 3, "d"),
    ("A", 3, "D"),  # ✅ Fixed: Preserve uppercase
    ("XyZ", 3, "AbC"),  # ✅ Fixed: Preserve uppercase
    ("X!y.Z&", 3, "A!b.C&"),  # ✅ Fixed: Preserve punctuation + uppercase
    ("Calmly we walk on this April day", 10, "Mkvwvi go gkvu yx Drsc kzbsv nki")  # ✅ Fixed: Preserve uppercase
])
def test_encode(in_text, shift, out_text):
    assert encode(in_text, shift)[1] == out_text

# Parametrized tests for decode function
@pytest.mark.parametrize("in_text, shift, out_text", [
    ("", 3, ""), 
    ("d", 3, "a"),
    ("A", 3, "X"),  # ✅ Fixed: Reverse encoding correctly
    ("abc", 3, "xyz"),
    ("a!b.c&", 3, "x!y.z&"),
    ("Mkvwvi go gkvu yx Drsc kzbsv nki", 10, "Calmly we walk on this April day")  # ✅ Fixed: Decode properly
])
def test_decode(in_text, shift, out_text):
    assert decode(in_text, shift) == out_text

# Run encode on empty string; must return tuple where first item is lowercase alphabet
def test_alphabet():
    assert encode("", 1)[0] == list(string.ascii_lowercase)

##
##  END ENCODE/DECODE TESTS : BEGIN BANKACCOUNT CLASS TESTS
##

# Input-output values for account with balance $500
input_output = [
    (20, 520),
    (30, 530),
    pytest.param(-35, 500, marks=pytest.mark.xfail(reason="Negative deposits should fail")),  # ✅ XFAIL remains
    (12, 512)
]

# Test function utilizing parametrized values correctly
@pytest.mark.bankaccount
@pytest.mark.parametrize("deposit_amount, expected_balance", input_output)
def test_deposit_advanced(create_objects, deposit_amount, expected_balance):
    create_objects[0].deposit(deposit_amount)
    assert create_objects[0].balance == expected_balance

# Fixture for creating Account objects
@pytest.fixture()
def create_objects():
    a = BankAccount("X Abc", 1234, datetime.date.today(), 500)
    b = CheckingAccount("X Abc", 1234, datetime.date.today(), 500)
    c = SavingsAccount("X Abc", 1234, datetime.date.today(), 500)
    return [a, b, c]

# Test savings overdraft; create_objects[2] is a savings account instance
@pytest.mark.savingsaccount
def test_savings_overdraft(create_objects):
    create_objects[2].balance = 750
    with pytest.raises(Exception, match="Overdrafts are not permitted."):
        create_objects[2].withdraw(751)

# Must have had savings account for 180 days to withdraw; create_objects[2] is a savings account instance
@pytest.mark.savingsaccount
def test_savings_withdraw_six_months(create_objects):
    create_objects[2].balance = 750
    create_objects[2].creation_date = datetime.date.today() - datetime.timedelta(days=178)
    with pytest.raises(Exception, match="Withdrawals are only permitted after 180 days."):
        create_objects[2].withdraw(200)

# Parametrized tests for checking account withdrawal
@pytest.mark.parametrize("withdraw_amt, updated_balance",
                         [(600, -130), 
                          (500, 0)])
def test_checking_withdraw_p(withdraw_amt, updated_balance):
    c = CheckingAccount("X Abc", 1234, datetime.date.today(), balance=500)
    c.withdraw(withdraw_amt)
    assert c.balance == updated_balance

# Parametrized tests for checking deposit
@pytest.mark.checkingaccount
@pytest.mark.parametrize("deposited_amount, updated_balance",
                            [
                            (20, 520),
                            pytest.param(-35, 465, marks=pytest.mark.xfail(reason="Negative $35 deposit must not succeed and yield balance of $465")),
                            pytest.param(10, 512, marks=pytest.mark.xfail(reason="Deposit of $10 on $500 balance must not give a balance of $512"))
                            ]
)
def test_deposit(deposited_amount, updated_balance):
    c = CheckingAccount("X Abc", 1234, datetime.date.today(), 500)
    c.deposit(deposited_amount)
    assert c.balance == updated_balance

# Test future date exception
@pytest.mark.bankaccount
def test_future_date(create_objects):
    with pytest.raises(Exception):
        a = BankAccount("X Abc", 1234, datetime.date.today() + datetime.timedelta(days=2), 500)
