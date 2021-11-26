import pandas as pd
import requests
import matplotlib.pyplot as plt



class Users:
    # This class represents a user in the stock market

    def __init__(self, UserID, UserName, CashBalance, Portfolio, Transactions):
        self.UserID = UserID
        self.UserName = UserName
        self.CashBalance = CashBalance
        self.Portfolio = Portfolio
        self.Transactions = Transactions
        f = open("UserList.txt", "a")
        f.write(str(self.UserID))
        f.close()

    def calculate_balance(self):
        total_balance = 0
        for k, v in self.Portfolio.items():
            balance = get_stocks_data(k)['close'].iloc[0] * v
            total_balance += balance

        print('Your current portfolio value is: ', round(total_balance, 2))
        return total_balance

user1 = Users(1, 'Python', 10000, {}, [])
# user2 = Users(1, 1, 1, {}, 1)


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

    print(df.head())
    return df


getStocksData('IBM')




#class Stocks:
    # This class represents the stocks in a stock market

#    def __init__(self,

def buy_stock(user, ticker, price, volume):
     total_price = price * volume
     if user.CashBalance <= total_price:
         print('You do not have enough cash balance')
     else:
        user.CashBalance -= total_price
        if ticker in user.Portfolio:
            user.Portfolio[ticker] += volume
        else:
            user.Portfolio[ticker] = volume
        print("You bought " + str(volume) + " shares in " + ticker + "! You now have " + str(user.Portfolio[ticker]) +
              " shares in this company.")
        temp = [ticker, price, volume] # TO BE ADDED: time and date of transaction
        user.Transactions.insert(0, temp)

buy_stock(user1, 'MSFT', 1.00, 10)
buy_stock(user1, 'IBM', 5.00, 20)
print(user1.CashBalance)
print(user1.Transactions)
print(user1.Portfolio)


def sell_stock(user, ticker, price, volume):
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
        temp = [ticker, price, -volume]  # TO BE ADDED: time and date of transaction
        user.Transactions.insert(0, temp)
    else:
        user.Portfolio.pop(ticker)
        user.CashBalance += price * volume
        print("You sold " + str(volume) + " shares in " + ticker + "! You now have no shares left in this company.")
        temp = [ticker, price, -volume]  # TO BE ADDED: time and date of transaction
        user.Transactions.insert(0, temp)

    # SellPrice = input("Please type for what price you want to sell each stock: ")
#sell_stock(user1, 'MSFT', 1.00, 10)
sell_stock(user1, 'IBM', 5.00, 10)
#sell_stock(user1, 'AAPL', 5.00, 20)
print(user1.CashBalance)
print(user1.Transactions)
print(user1.Portfolio)


def plotStocksData(user):
    # looping through all stocks in the portfolio
    for k in user.Portfolio:
        print(k)
        df = getStocksData(k)
        plt.plot(df['close'], label=k)
    plt.legend()
    plt.show()

plotStocksData(user1)