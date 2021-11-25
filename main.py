import pandas as pd

UserID = input("Please type in your UserID: ")
UserName = input("Please type in your name and press Enter: ")
CashBalance = input("Your current Cash Balance is: ")
Portfolio = input("Please enter your stock portfolio: ")

class Users:
    # This class represents a user in the stock market

    def __init__(self, UserID, UserName, CashBalance, Portfolio):
        self.UserID = UserID
        self.UserName = UserName
        self.CashBalance = CashBalance
        self.Portfolio = []

user1 = Users(UserID, UserName, CashBalance, Portfolio)
#user1 = Users(1, 'Michelle', 5000, ['stock1', 'stock2'])
