# TODO: Aquisição BOVA11
# TODO: Aquisição VALE3
# TODO: Aquisição ITUB4
# TODO: Aquisição BIDI4
# TODO: Aquisição ABEV3
# TODO: Aquisição SQIA3
# ! Utilizar apenas dia util
# * https://www.statsmodels.org/stable/examples/notebooks/generated/exponential_smoothing.html

from datetime import datetime
import math
import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf

def main():
    # Definindo ticker
    ticker = {"Inter": "BIDI4.SA", "Petrobras": "PETR4.SA"}

    currentTicker = ticker["Petrobras"]

    # Usando pandas datareader
    dataFrame = pd.DataFrame(pandasDataReader(currentTicker)).round(15)






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
