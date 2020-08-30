import math
from collections import defaultdict

import numpy as np

from datetime import datetime

import sys
from datetime import datetime
import math
import matplotlib.pyplot as plt
import mysql.connector
from mysql.connector import Error
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf


class MySQLManager():
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
            host=self.DB_HOST,
            user=self.DB_USER,
            passwd=self.DB_PASSWORD,
            db=self.DB_NAME
        )
        self.db_cursor = self.db_connection.cursor()

        return

    def create(self, table_name, ticker, data_frame, verbose):
        sql = ("INSERT INTO "+table_name+" "
               "(ticker, date, open, high, low, close, adj_close, volume) "
               " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

        for index, dayStockValue in data_frame.iterrows():
            if verbose:
                print("Indice [" + str(index) + "]: ", end="")
                print(dayStockValue['Open'], dayStockValue['High'], dayStockValue['Low'], dayStockValue['Close'], dayStockValue['Adj Close'], dayStockValue['Volume'], sep="\t")
            data_dict = defaultdict(any)
            data_dict['ticker'] = ticker
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
            if self.db_cursor.execute(sql, value) == 0:
                print("db_cursor.execute equals to zero.")
                sys.exit(-1)

        self.db_connection.commit()

        if verbose:
            print(self.db_cursor.rowcount, "record inserted.")

        self.db_connection.close()
        return self.db_cursor.rowcount

    def read(self, table_name, ticker, where_condition,verbose):
        result = {}
        try:
            sql_select_Query = "select " + "ticker, date, adj_close" + " from " + self.DB_NAME + "." + table_name + " where ticker = \"" + ticker + "\" "

            if where_condition is None:
                sql_select_Query = sql_select_Query + ";"
            else:
                sql_select_Query = sql_select_Query + " AND " + where_condition + ";"

            self.db_cursor.execute(sql_select_Query)
            records = self.db_cursor.fetchall()
            for row in records:
                if row[0] == ticker:
                    if verbose:
                        print("Date = " + row[1].strftime("%Y-%m-%d") + "\tadj_close  = " + str(row[2]))
                    result[row[1]] = row[2]
                else:
                    print("Wrong ticker.")
                    sys.exit(-2)
            sql_select_Query = None
        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if self.db_connection.is_connected():
                self.db_connection.close()
                self.db_cursor.close()
        return result

    def update(self, table_name, data, where_condition):
        # TODO: Fazer função de atualização do banco de dados;
        return

    def delete(self, table_name, where_condition):
        # TODO: Fazer função de remoção do banco de dados;
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
