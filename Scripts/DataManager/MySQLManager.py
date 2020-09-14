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
from sqlalchemy import create_engine


class MySQLManager():
    DB_HOST = ""
    DB_USER = ""
    DB_PASSWORD = ""
    DB_NAME = ""
    db_connection = None
    db_cursor = None

    db_engine = None

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

        self.db_engine = create_engine("mysql+pymysql://{user}:{passwd}@{host}/{db}"
                               .format(user=self.DB_USER,
                                       passwd=self.DB_PASSWORD,
                                       host=self.DB_HOST,
                                       db=self.DB_NAME))

        return

    def create(self, table_name, data_frame, insertion_type):
        data_frame.to_sql(table_name, con=self.db_engine, if_exists=insertion_type)
        self.db_connection.close()

    def read(self, table_name_or_query):
        result = pd.read_sql(table_name_or_query, con=self.db_engine)
        self.db_connection.close()
        return result