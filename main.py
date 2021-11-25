import pandas as pd


class Users:
    # This class represents a user in the stock market

    def __init__(self, UserID, UserName, CashBalance, Portfolio):
        self.UserID = input("Please type in your UserID: ")
        self.UserName = input("Please type in your name and press Enter: ")
        self.CashBalance = input("Your current Cash Balance is: ")
        self.Portfolio = []


user1 = Users()
