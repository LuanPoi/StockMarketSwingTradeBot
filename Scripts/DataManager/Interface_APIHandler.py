import abc


class Interface_APIHandler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, api_key):
        return

    @abc.abstractmethod
    def connect(self, ticker):
        """
        # * Faz a requisicao com a API e armazena o objeto retornado para ser utilizado pelas outras funcoes;
        # ? Armazena o retorno para ser utilizado nas outras funcoes;
        """
        return

    @abc.abstractmethod
    def historical(self, start_date, end_date):
        """
        # * Retorna os dados historicos da acao em uma lista de strings;
        # ? Caso o valor de start_date e end_date for igual a nulo será retornado o periodo maximo;
        """
        return
