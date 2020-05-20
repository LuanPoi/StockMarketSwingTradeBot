import math
import numpy as np

from datetime import datetime
from Scripts.DataManager import Interface_DBManager

import mysql.connector
from datetime import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf


class MySQLManager(Interface_DBManager):
    DB_HOST = ""
    DB_USER = ""
    DB_PASSWORD = ""
    DB_NAME = ""
    db_connection = None
    db_cursor = None

    def __init__(self, host, user, password):
        self.DB_HOST = host
        self.DB_USER = user
        self.DB_PASSWORD = password

        return

    def connect(self, database_name):
        self.DB_NAME = database_name

        self.db_connection = mysql.connector.connect(
            self.DB_HOST,
            self.DB_USER,
            self.DB_PASSWORD,
            self.DB_NAME
        )
        self.db_cursor = self.db_connection.cursor()

        return

    def create(self, table_name, data_frame, verbose):
        sql = ("INSERT INTO "+table_name+" "
               "(ticker, date, open, high, low, close, adj_close, volume) "
               " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

        for index, dayStockValue in data_frame.iterrows():
            if verbose:
                print("Indice [" + str(index) + "]: ", end="")
                print(dayStockValue['Open'], dayStockValue['High'], dayStockValue['Low'], dayStockValue['Close'], dayStockValue['Adj Close'], dayStockValue['Volume'], sep="\t")
            data_dict = []
            data_dict['date'] = datetime.date(index)
            data_dict['open'] = dayStockValue['Open']
            data_dict['high'] = dayStockValue['High']
            data_dict['low'] = dayStockValue['Low']
            data_dict['close'] = dayStockValue['Close']
            data_dict['adj_close'] = dayStockValue['Adj Close']
            data_dict['volume'] = dayStockValue['Volume']

            data_dict = self.parse_data(data_dict)
            value = (data_dict['ticker'], data_dict['date'], data_dict['open'], data_dict['high'], data_dict['low'],
                     data_dict['close'], data_dict['adj_close'], data_dict['volume'])
            self.db_cursor.execute(sql, value)

        self.db_connection.commit()

        if verbose:
            print(self.db_cursor.rowcount, "record inserted.")

        return self.db_cursor.rowcount

    def read(self, table_name, where_condition):
        return

    def update(self, table_name, data, where_condition):
        return

    def delete(self, table_name, where_condition):
        return

    def parse_data(self, data_dict):
        if math.isnan(data_dict['open']):
            data_dict['open'] = 0
        else:
            data_dict['open'] = "{:18.15f}".format(data_dict['open'])
        if math.isnan(data_dict['high']):
            data_dict['high'] = 0
        else:
            data_dict['high'] = "{:18.15f}".format(data_dict['high'])
        if math.isnan(data_dict['low']):
            data_dict['low'] = 0
        else:
            data_dict['low'] = "{:18.15f}".format(data_dict['low'])
        if math.isnan(data_dict['close']):
            data_dict['close'] = 0
        else:
            data_dict['close'] = "{:18.15f}".format(data_dict['close'])
        if math.isnan(data_dict['adj_close']):
            data_dict['adj_close'] = 0
        else:
            data_dict['adj_close'] = "{:18.15f}".format(data_dict['adj_close'])
        if math.isnan(data_dict['volume']):
            data_dict['volume'] = 0
        else:
            data_dict['volume'] = int(data_dict['volume'])

        return data_dict