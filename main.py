import json
import random
import pandas as pd
import requests
import matplotlib.pyplot as plt
from pydantic import BaseModel

# readInUsers
f = open('data.json', 'r')
try:
    allUsers = json.loads(f.read())
except:
    allUsers = {}
f.close()

# Overall starting date: 04/01/2010
f = open('date.txt', 'r')
currentDate = int(f.read())
f.close()


class Users2(BaseModel):
    UserName: str
    CashBalance: int
    Portfolio: dict
    Transactions: list


def new_user():
    UserNameTemp = input("Please enter your new username and press Enter: ")
    f = open("UserList.txt", "r")
    userlist = f.read().splitlines()
    f.close()
    if UserNameTemp in userlist:
        print("This user name already exists!")
        return
    else:
        print("Welcome,", UserNameTemp)
        CashBalanceTemp = float(input("Please enter your current cash balance and Press Enter: $"))
        f = open("UserList.txt", "a")
        f.write(str(UserNameTemp) + "\n")
        f.close()
        user = Users2(UserName=UserNameTemp, CashBalance=CashBalanceTemp, Portfolio={},
                      Transactions=[])
        return user


def login():
    newuser = 0
    while newuser not in ["y", "n"]:
        newuser = input("Welcome to the Investment Game! Are you a new user? Y/N: ").lower()
    if newuser == "y":
        userCurrent = new_user()
        try:
            userjson = userCurrent.json()
            allUsers[userCurrent.UserName] = userjson
            f = open('data.json', 'w')
            f.write(json.dumps(allUsers, indent=4))
            f.close()
        except:
            print("")
        return userCurrent
    else:
        name = input("Enter your user name: ")
        f = open("UserList.txt", "r")
        userlist = f.read().splitlines()
        f.close()
        if name in userlist:
            # read in data from file on user
            print("Welcome back, ", name)
            userCurrent = Users2.parse_raw(allUsers[name])
            return userCurrent
        else:
            print("This user does not exist")
            userCurrent = None
            return userCurrent


# this function will return the correct stocks data corresponding to the ticker
# more can be found on 'search endpoint', but let's use this list for now
# IBM - IBM
# Tesco - TSCO.LON
# Shopify - SHOP.TRT
# GreenPower Motor Company - GPV.TRV
# Daimler - DAI.DEX
# Reliance Industries Limited - RELIANCE.BSE
# SAIC Motor Corporation - 600104
# China Vanke Company - 000002


def calculate_balance(user):
    total_balance = 0
    for k, v in user.Portfolio.items():
        balance = getStocksData(k)['close'].iloc[0] * v
        total_balance += balance

    print('Your current portfolio value is: $', round(total_balance, 2))
    return total_balance

def getStocksData(ticker):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&outputsize=full&apikey=demo'
    r = requests.get(url)
    if r.status_code != 200:
        raise ValueError("Could not retrieve data, code:", r.status_code)

    raw_data = r.json()

    data = raw_data['Time Series (Daily)']
    df = pd.DataFrame(data).T.apply(pd.to_numeric)

    df.index = pd.DatetimeIndex(df.index)
    df.rename(columns=lambda s: s[3:], inplace=True)

    # print(df.head())
    return df


# data = getStocksData('IBM')


def buy_stock(user, ticker, price, volume, date):
    total_price = price * volume
    if user.CashBalance <= total_price:
        print('You do not have enough cash to buy this many stocks!')
    else:
        user.CashBalance -= total_price
        if ticker in user.Portfolio:
            user.Portfolio[ticker] += volume
        else:
            user.Portfolio[ticker] = volume
        print("You bought " + str(volume) + " shares in " + ticker + "! You now have " + str(user.Portfolio[ticker]) +
              " shares in this company.")
        temp = [ticker, price, volume, date] # TO BE ADDED: time and date of transaction
        user.Transactions.insert(0, temp)
        userjson = user1.json()
        allUsers[user1.UserName] = userjson

#
# currentDate = buy_stock(user1, 'MSFT', 1.00, 10, currentDate)
# currentDate = buy_stock(user1, 'IBM', 5.00, 20, currentDate)
# # print(user1.CashBalance)
# # print(user1.Transactions)
# # print(user1.Portfolio)
# print(currentDate)

def sell_stock(user, ticker, price, volume, date):
    if ticker not in user.Portfolio:
        print("You do not have this stock in your portfolio")
        return

    currentVolume = user.Portfolio[ticker]
    if currentVolume < volume:
        print("You do not have enough stocks in your Portfolio to sell")
        return
    elif currentVolume > volume:
        user.Portfolio[ticker] -= volume
        user.CashBalance += price * volume
        print("You sold " + str(volume) + " shares in " + ticker + "! You have " + str(user.Portfolio[ticker]) +
              " shares remaining.")
        temp = [ticker, price, -volume, date]  # TO BE ADDED: time and date of transaction
        user.Transactions.insert(0, temp)
    else:
        user.Portfolio.pop(ticker)
        user.CashBalance += price * volume
        print("You sold " + str(volume) + " shares in " + ticker + "! You now have no shares left in this company.")
        temp = [ticker, price, -volume, date]  # TO BE ADDED: time and date of transaction
        user.Transactions.insert(0, temp)

    userjson = user1.json()
    allUsers[user1.UserName] = userjson


# #sell_stock(user1, 'MSFT', 1.00, 10)
# sell_stock(user1, 'IBM', 5.00, 10)
# #sell_stock(user1, 'AAPL', 5.00, 20)
# print(user1.CashBalance)
# print(user1.Transactions)
# print(user1.Portfolio)

# f = open('data.json', 'w')
# f.write(json.dumps(allUsers, indent=4))
# f.close()

def plot_stocks_prices(ticker):
    df = getStocksData(ticker)
    plt.plot(df['close'], label=ticker)
    plt.legend()
    plt.show()



def plotStocksData(user):
    # looping through all stocks in the portfolio
    for k in user.Portfolio:
        print(k)
        df = getStocksData(k)
        plt.plot(df['close'], label=k)
    plt.legend()
    plt.show()

# plotStocksData(user1)

#View cash balance
def current_cashbalance(user):
    print("Your current cash balance is ", user.CashBalance, ".")





user1 = login()

counter = 1
while counter < 5000:
    print("\n \n \n \n")
    print("What would you like to do? \n -- Quit: Quit the program and save progress. \n -- Buy: Buy a stock. \n -- Sell:"
          "Sell a stock. \n -- View: View the performance graph of a single stock. \n -- Balance: Check your balance. \n "
          "-- Portfolio: Check the contents of your portfolio. \n -- Assets: View the current value of all your assets.")
    answer = input("Enter your choice and press Enter: ").lower()
    if answer == "quit" or answer == "q":
        break
    elif answer == "buy" or answer == "b":
        stock = input("Which stock would you like to buy? Enter the ticker and press Enter: ")
        try:
            data = getStocksData(stock)
            print("The stock price today is $" + str(data.iloc[currentDate]['close']) + ".")
            amount = int(input("How many stocks would you like to buy? Enter a valid amount and press Enter: "))
            buy_stock(user1, stock, data.iloc[currentDate]['close'], amount, data.iloc[currentDate].name)
            currentDate -= random.randint(1, 14)
            # print(currentDate)
            f = open('date.txt', 'w')
            f.write(str(currentDate))
            f.close()
        except:
            print("Something went wrong. Please try again.")
    elif answer == "sell" or answer == "s":
        stock = input("Which stock would you like to sell? Insert the ticker and press Enter: ")
        data = getStocksData(stock)
        try:
            print("You currently have", user1.Portfolio[stock], "stocks in this company. ")
            try:
                data = getStocksData(stock)
                amount = int(input("How many would you like to sell? Enter a valid amount and press Enter: "))
                print("The stock market price today is $" + str(data.iloc[currentDate]['close']) + ".")
                sell_stock(user1, stock, data.iloc[currentDate]['close'], amount, currentDate)
                currentDate -= random.randint(1, 14)
                f = open('date.txt', 'w')
                f.write(str(currentDate))
                f.close()
            except:
                print("Something went wrong. Please try again.")
        except:
            print("You do not have any stocks in this company!")
    elif answer == "view" or answer == "v":
        stock = input("Which stock performance graph would like to view? Insert the ticker and press Enter: ")
        plot_stocks_prices(stock)
        # Performance = plotStocksData(stock)
    elif answer == "balance" or answer == "b":
        current_cashbalance(user1)
    elif answer == "portfolio" or answer == "p":
        for k,v in user1.Portfolio.items():
            print('You have', v, 'share(s) in company', k)
    elif answer == "assets" or answer == "a":
        calculate_balance(user1)
    else:
        print("That is not a valid option! Try again.")
    counter += 1


f = open('data.json', 'w')
f.write(json.dumps(allUsers, indent=4))
f.close()