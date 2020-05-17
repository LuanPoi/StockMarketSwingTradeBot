# TODO: Aquisição BOVA11
# TODO: Aquisição VALE3
# TODO: Aquisição ITUB4
# TODO: Aquisição BIDI4
# TODO: Aquisição ABEV3
# TODO: Aquisição PETR4
# TODO: Aquisição SQIA3
# ! Utilizar apenas dia util

from datetime import datetime
import math
import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf


def main():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="toor",
        database="stock_market"
    )
    mycursor = mydb.cursor()

    # Definindo ticker
    ticker = {"Inter": "BIDI4.SA", "Petrobras": "PETR4.SA"}

    currentTicker = ticker["Petrobras"]

    # Usando pandas datareader
    dataFrame = pd.DataFrame(pandasDataReader(currentTicker)).round(15)

    sql = ("INSERT INTO stock "
           "(ticker, date, open, high, low, close, adj_close, volume) "
           " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

    for index, dayStockValue in dataFrame.iterrows():
        # print("Indice ["+str(index)+"]: ", end="")
        # print(dayStockValue['Open'], dayStockValue['High'], dayStockValue['Low'], dayStockValue['Close'], dayStockValue['Adj Close'], dayStockValue['Volume'], sep="\t")
        date = datetime.date(index)
        open = dayStockValue['Open']
        high = dayStockValue['High']
        low = dayStockValue['Low']
        close = dayStockValue['Close']
        adj_close = dayStockValue['Adj Close']
        volume = dayStockValue['Volume']

        if math.isnan(open):
            open = 0
        else:
            open = "{:18.15f}".format(open)
        if math.isnan(high):
            high = 0
        else:
            high = "{:18.15f}".format(high)
        if math.isnan(low):
            low = 0
        else:
            low = "{:18.15f}".format(low)
        if math.isnan(close):
            close = 0
        else:
            close = "{:18.15f}".format(close)
        if math.isnan(adj_close):
            adj_close = 0
        else:
            adj_close = "{:18.15f}".format(adj_close)
        if math.isnan(volume):
            volume = 0
        else:
            volume = int(volume)

        value = (currentTicker, date, open, high, low, close, adj_close, volume)
        mycursor.execute(sql, value)

    mydb.commit()
    print(mycursor.rowcount, "record inserted.")


def pandasDataReader(ticker):
    yf.pdr_override()  # <== that's all it takes :-)
    data = pdr.data.get_data_yahoo(ticker, period="max")
    return data


def printagrafico(data, ticker):
    # Plot the adjusted close price
    data['Close'].plot(figsize=(10, 7))
    # Define the label for the title of the figure
    plt.title("Adjusted Close Price of %s" % ticker, fontsize=16)
    # Define the labels for x-axis and y-axis
    plt.ylabel('Price', fontsize=14)
    plt.xlabel('Year', fontsize=14)
    # Plot the grid lines
    plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
    # Show the plot
    plt.show()


if __name__ == "__main__":
    main()
