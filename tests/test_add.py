## INTRO ABOUT TESTING 

from .additon import calculations,sub, BankAccount, InsufficientFunds
import pytest 


@pytest.fixture
def zero_bankAccount():
    return BankAccount()

@pytest.fixture
def def_bankaccount():
    return BankAccount(140)



@pytest.mark.parametrize("num1, num2, expected",[
    (1,2,3),
    (4,5,9),
    (1,2,3),
    (12,13,25),
    (12,13,25)
] )

def test_add(num1, num2, expected):
    print("Testing Ongoiing")
    assert calculations(num1,num2) == expected


def test_sub():
    assert sub(51,6)==45
    

# Testing for the class /

def test_bank_set_accont_detail(def_bankaccount):
    print("This is the current Balance")
    assert def_bankaccount.balance==140
    
    
def test_bank_deposit(def_bankaccount): 
    def_bankaccount.deposit(40)
    print("This is the current Balance")
    assert def_bankaccount.balance==180
    
def test_withdraw(def_bankaccount): 
    def_bankaccount.withdraw(10)
    print("This is the current Balance")
    assert def_bankaccount.balance==130
    
def test_interest(def_bankaccount): 
    def_bankaccount.interest(1.4)
    print("This is the current Balance")
    assert def_bankaccount.balance==196
    

def test_bankaccount(zero_bankAccount):
    zero_bankAccount.deposit(1000)
    zero_bankAccount.withdraw(400)
    print("This is the current Balance")
    assert zero_bankAccount.balance==600
    
@pytest.mark.parametrize("deposited, withdrawed, expected", [
    (100,50,50),
    (400,220,180),
    (1000,500,500) 
])

def test_acccount_full_details_with_mark(zero_bankAccount,  deposited, withdrawed, expected):
    zero_bankAccount.deposit(deposited)
    zero_bankAccount.withdraw(withdrawed)
    print("This is my markParameterized method for bankaccount")
    assert zero_bankAccount.balance==expected
    
def test_insufficient_funds(zero_bankAccount):
    with pytest.raises(InsufficientFunds):
        zero_bankAccount.withdraw(100)