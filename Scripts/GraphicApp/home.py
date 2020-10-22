from tkinter import *
from datetime import datetime
import pandas as pd
import numpy as np
from stockstats import StockDataFrame
import csv
import sys
import math

import pandas_datareader as pdr
import yfinance as yf
import statsmodels as sm
import matplotlib as mpl

tickers = {
    "Inter": "BIDI4.SA",
    "Petrobras": "PETR4.SA",
    "Vale": "VALE3.SA",
    "Itau": "ITUB4.SA",
    "Ambev": "ABEV3.SA",
    "Sinqia": "SQIA3.SA",
    "Bovespa": "BOVA11.SA"
}

class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(master)
        self.quartoContainer["padx"] = 20
        self.quartoContainer.pack()

        self.ultimoContainer = Frame(master)
        self.ultimoContainer["pady"] = 20
        self.ultimoContainer.pack()

        #---------------------------------------

        self.titulo = Label(self.primeiroContainer, text="Simulador de investimentos simples")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()

        # ---------------------------------------
        self.acaoLabel = Label(self.segundoContainer, text="Ação", font=self.fontePadrao)
        self.acaoLabel.pack(side=LEFT)

        self.acao_selecionada = StringVar(self.segundoContainer)
        self.acao_selecionada.set("BIDI4")
        self.acao = OptionMenu(self.segundoContainer, self.acao_selecionada, "PETR4", "VALE3", "ITUB4", "ABEV3", "SQIA3", "BOVA11")
        self.acao.config(width=10, font=('Helvetica', 12))
        self.acao.pack()
        self.acao_selecionada.trace("w", self.pegaValorDaAcao)

        # ---------------------------------------

        valor_acao_label = Label(self.terceiroContainer, text="Ação", font=self.fontePadrao)
        self.acaoLabel.pack(side=LEFT)

        # ---------------------------------------

        self.valorLabel = Label(self.quartoContainer,text="Esta ação esta custando: ", font=self.fontePadrao)
        self.valorLabel.pack(side=LEFT)

        self.valor = Entry(self.quartoContainer)
        self.valor["width"] = 30
        self.valor["font"] = self.fontePadrao
        self.valor.pack(side=LEFT)

        # ---------------------------------------

        self.autenticar = Button(self.ultimoContainer)
        self.autenticar["text"] = "Investir"
        self.autenticar["font"] = ("Calibri", "8")
        self.autenticar["width"] = 12
        self.autenticar["command"] = self.verificaSenha
        self.autenticar.pack()

        self.mensagem = Label(self.ultimoContainer, text="", font=self.fontePadrao)
        self.mensagem.pack()

    #TODO:
    #Método verificar senha
    def verificaSenha(self):
        usuario = self.nome.get()
        senha = self.senha.get()
        if usuario == "usuariodevmedia" and senha == "dev":
            self.mensagem["text"] = "Autenticado"
        else:
            self.mensagem["text"] = "Erro na autenticação"

    def pegaValorDaAcao(self, *args):
        dataset_base_path = "../../Resources/Datasets/"
        ticker_metadata = \
            pd.read_csv(dataset_base_path + 'stock_metadata' + '.csv', sep=';', quotechar='"', names=['dtypes'],
                        index_col=0).to_dict()['dtypes']
        data = pd.read_csv(dataset_base_path + 'stock.csv', sep=';', header=0, index_col=0,
                           quoting=csv.QUOTE_NONNUMERIC,
                           dtype=ticker_metadata)
        data.index = pd.to_datetime(data.index)
        data = data.loc[data['ticker'] == (self.acao_selecionada.get()+'.SA')]
        training_data = float(data['adj close'].tail(1))
        self.valorLabel.config(text="Esta ação esta custando: {}".format(training_data))


root = Tk()
Application(root)
root.mainloop()