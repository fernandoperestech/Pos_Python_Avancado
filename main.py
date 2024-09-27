import os
import logging
import openpyxl
import subprocess
import pandas as pd
import yfinance as yf
import investpy as inv
from datetime import datetime
from dateutil.relativedelta import relativedelta

logging.basicConfig(filename='logs/logsSistem.log', encoding='utf-8', level=logging.DEBUG)

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
        workbook.save('data/investpy_tickers_b3.xlsx')

    except Exception as e:
        logging.warning(f'main.get_ativos(): {str(e)}')

''' Buscando ativos da B3 e gravando no arquivo -> data\tickers_investpy.xlsx'''
get_ativos()

''' Definição da função que coletará os dados dos papéis da B3 '''
def obter_dados(ticker, start_date, end_date):
    try:
        # Faz o download dos dados históricos do ticker
        dados_ticker = yf.download(ticker, start=start_date, end=end_date)
        
        if dados_ticker.empty:
            logging.warning(f'Dados não encontrados para {ticker}.')
            return pd.DataFrame()  # Retorna DataFrame vazio se não houver dados

        # Adiciona a coluna do ticker e de data
        dados_ticker['Ticker'] = ticker
        dados_ticker['Data'] = dados_ticker.index

        # Reorganiza as colunas na ordem desejada
        dados_ticker = dados_ticker[['Ticker', 'Data', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
        
        return dados_ticker
    except Exception as e:
        logging.warning(f'Erro ao obter dados para {ticker}: {str(e)}')
        return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro

def verificar_e_criar_arquivo(caminho):
    # Verifica se o arquivo existe, caso contrário, irá criar o arquivo
    try:
        open(caminho, 'a').close()  # Cria o arquivo se não existir
    except Exception as e:
        logging.warning(f'Erro ao verificar/criar arquivo: {str(e)}')

# Função principal para buscar os dados
def iniciar_busca_dados():
    try:
        caminho_tickers = 'data/tickers_investpy.xlsx'

        # Carrega os tickers do arquivo Excel
        tickers_df = pd.read_excel(caminho_tickers, usecols=[0], skiprows=1, header=None, names=['Ticker'])

        tickers = tickers_df['Ticker'].tolist()

        end_date = datetime.now()
        start_date = end_date - relativedelta(months=4)

        formated_end_date = end_date.strftime("%Y-%m-%d")
        formated_start_date = start_date.strftime("%Y-%m-%d")

        caminho_dados = 'data/yfinance_tickers_results.csv'

        # Verifica e cria arquivo para armazenar os dados
        verificar_e_criar_arquivo(caminho_dados)

        dados_totais = pd.DataFrame()

        for ticker in tickers:
            ticker = ticker + '.SA'
            print(f"Buscando dados para: {ticker}")
            dados_ticker = obter_dados(ticker, formated_start_date, formated_end_date)

            if not dados_ticker.empty:
                dados_totais = pd.concat([dados_totais, dados_ticker])

        if not dados_totais.empty:
            # Salva todos os dados no arquivo CSV
            dados_totais.to_csv(caminho_dados, index=False)

    except Exception as e:
        logging.warning(f'Erro ao iniciar busca de dados: {str(e)}')

# Executa a função principal
iniciar_busca_dados()