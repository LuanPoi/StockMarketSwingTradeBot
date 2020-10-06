from datetime import datetime
import math
import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf

def historical(ticker, start_date = None, end_date = None):
    if ticker is not None:
        yf.pdr_override()
        if start_date is not None and end_date is not None:
            data = pdr.data.get_data_yahoo(ticker=ticker, start=start_date, end=end_date)
            return data
        if start_date is None and end_date is None:
            data = pdr.data.get_data_yahoo(ticker, period="max")
            return data
    print("YahooAPIHandler: Valores invalidos.")
    return None
