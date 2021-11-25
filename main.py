import pandas as pd
import requests


class Users:
    # This class represents a user in the stock market

    def __init__(self, UserID, UserName, CashBalance, Portfolio, Transactions):
        self.UserID = input("Please type in your UserID: ")
        self.UserName = input("Please type in your name and press Enter: ")
        self.CashBalance = float(input("Your current Cash Balance is: "))
        self.Portfolio = {}
        self.Transactions = []
# write to txt file

user1 = Users(1, 1, 1, {}, 1)
# user2 = Users(1, 1, 1, 1, 1)


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

    return df.head()


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
        temp = [ticker, price, volume]
        user.Transactions.append(temp)

buy_stock(user1, 'MSFT', 1.00, 10)
