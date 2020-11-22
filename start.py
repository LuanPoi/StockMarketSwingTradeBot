# O que o usuário pode fazer no programa:
#
# 1- Baixar/Atualizar a base de dados de uma ação;
# python3 start.py <stock> --update
# 2- Executar o programa inteiro;
# python3 start.py <stock>
# 3- Executar o programa carregando os modelos ja treinados;
# python3 start.py <stock> --load-models
# 6- Gerar avaliações de uma previsão;
# vai ser uma opção
# 7- Gerar os gráficos da previsão e das avaliações;
# vai ser uma opção
# 8- Listar os tickers disponíveis para uso
# python3 start.py --stocks

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import Scripts.DataManager as dm
from os import system, name

tickers = {
    "Inter": "BIDI4.SA",
    "Petrobras": "PETR4.SA",
    "Vale": "VALE3.SA",
    "Itau": "ITUB4.SA",
    "Ambev": "ABEV3.SA",
    "Sinqia": "SQIA3.SA",
    "Bovespa": "BOVA11.SA"
}

def main():
    params = sys.argv[1:]
    selectedTicker  = ""
    estados = {
        "update": False,
        "load-models": False,
    }

    if len(params) < 1:
        clearScreen()
        print("Comando incorreto, por favor insira o comando seguindo a sequência:")
        print("\npython3 start.py <acao> [opções]")
        print("\n\nPara ver a lista de ações disponíveis digite 'python3 start.py --stocks' sem as aspas.")
        return

    if params[0] == "--stocks":
        listaTickers()
        return
    elif params[0] not in tickers.keys():
        clearScreen()
        print("Ação inválida")
        print("\n\nPara ver a lista de ações disponíveis digite 'python3 start.py --stocks' sem as aspas.")
        return
    else:
        selectedTicker = tickers[params[0]]

    for i in range(len(params)):
        if params[i] == "--load-models":
            estados['load-models'] = True
        elif params[i] == "--update":
            estados['update'] = True

    dm.run(ticker = selectedTicker, update = estados['update'], loadModels = estados['load-models'], path = os.getcwd())


def listaTickers():
    clearScreen()
    print("Lista de ações disponíveis:")
    for tickerKey in tickers.keys():
        print(f"\t- {tickerKey}")


def clearScreen():
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


if __name__ == "__main__":
    main()