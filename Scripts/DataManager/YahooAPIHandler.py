from datetime import datetime
import math
import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf

class YahooAPIHandler():
    API_KEY = ""

    def __init__(self, api_key):
        if api_key is not None:
            self.API_KEY = str(api_key)
        return

    def historical(self, ticker, start_date, end_date):
        if ticker is not None:
            yf.pdr_override()  # <== that's all it takes :-)
            if start_date is not None and end_date is not None:
                data = pdr.data.get_data_yahoo(ticker=ticker, start=start_date, end=end_date)
                return data
            if start_date is None and end_date is None:
                data = pdr.data.get_data_yahoo(ticker, period="max")
                return data
        print("YahooAPIHandler: Valores invalidos.")
        return None
