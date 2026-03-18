# Dummy data for understanding the testingg 

def calculations(a:int, b :int):
    return a+b 

def sub(a:int, b :int):
    return a-b 


class InsufficientFunds(Exception):
    pass

class BankAccount():
    def __init__(self, startingBalance=0):
         self.balance=startingBalance
         
    def deposit(self, amount):
        self.balance+=amount
        
    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds("Insufficient amount in the account")
        self.balance-=amount
        
    def interest(self, rate):
        self.balance*=rate