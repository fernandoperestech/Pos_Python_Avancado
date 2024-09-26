import os
import logging
import openpyxl
import subprocess
import pandas as pd
import yfinance as yf
import investpy as inv


''' função para criar estrutura de pastas, para receber dados e registrar os Logs do sistema '''
def folder_create(folder_list : list):
    try:
        if len(folder_list)>0:
            for folder in folder_list:
                if not os.path.exists(folder):
                    try:
                        os.makedirs(folder)
                    except OSError as e:
                        print(e)
                else:
                    pass
        else:
             pass 
    except Exception as e:
        logging.warning(f'main.folder_create(): {str(e)}')

''' Verificando estrutura de pastas do projeto e criando, caso não exista '''
folder_create(['logs', 'data', 'processedData'])

''' função para buscar lista de ativos da B3 '''
def get_ativos():
    try:
        brs = inv.stocks.get_stocks(country='brazil')
        lista_ativos_investpy = [] 
        for key, value in brs.iterrows():
            ativo = (value['symbol'])
            lista_ativos_investpy.append(ativo)
        cabecalho = 'Tickers'
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.cell(row=1, column=1, value=cabecalho)
        
        for index, item in enumerate(lista_ativos_investpy, start=1):
            sheet.cell(row=index, column=1, value=item)
        workbook.save('data/tickers_investpy.xlsx')

    except Exception as e:
        logging.warning(f'main.get_ativos(): {str(e)}')

''' Buscando ativos da B3 e gravando no arquivo -> data\tickers_investpy.xlsx'''
get_ativos()

''' BLOCO DE CÓDIGO PARA OBTENÇÃO DOS DADOS DOS ATIVOS '''

def obter_dados(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start=start_date, end=end_date)

        data['Ticker'] = ticker
        data['Data'] = data.index
        
        data = data[['Ticker', 'Data', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]

        return data
    
    except Exception as e:
        logging.warning(f'main.obter_dados(): {str(e)}')

def verificar_e_criar_arquivo(path):
    try:
        if not os.path.exists(path):
            dados_vazios = pd.DataFrame()
            dados_vazios.to_csv(path, index=False)
    except Exception as e:
        logging.warning(f'main.verificar_e_criar_arquivo(): {str(e)}')



