import abc


class Interface_DBManager(metaclass=abc.ABCMeta):


    @abc.abstractmethod
    def __init__(self, host, user, password):
        return

    @abc.abstractmethod
    def connect(self, database_name):
        return

    @abc.abstractmethod
    def create(self, table_name, data):
        return

    @abc.abstractmethod
    def read(self, table_name, where_condition):
        return

    @abc.abstractmethod
    def update(self, table_name, data, where_condition):
        return

    @abc.abstractmethod
    def delete(self, table_name, where_condition):
        return
