# TODO: Aquisição BOVA11
# TODO: Aquisição VALE3
# TODO: Aquisição ITUB4
# TODO: Aquisição BIDI4
# TODO: Aquisição ABEV3
# TODO: Aquisição PETR4
# TODO: Aquisição SQIA3
# ! Utilizar apenas dia util

import matplotlib.pyplot as plt
from datetime import datetime
from pandas_datareader import data as pdr
import yfinance as yf


def main():
    # Definindo ticker
    ticker = {"Inter": "BIDI4.SA", "Petrobras": "PETR4.SA"}

    # Usando pandas datareader
    data = pandasDataReader(ticker["Petrobras"])
    print(data)


def pandasDataReader(ticker):
    yf.pdr_override()  # <== that's all it takes :-)
    data = pdr.get_data_yahoo(ticker, datetime(2015, 1, 1), datetime(2020, 5, 14))
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
