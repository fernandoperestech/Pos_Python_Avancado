import sys
import time
import progressbar
from tqdm import tqdm
from rich.progress import Progress
from alive_progress import alive_bar

import json
import os
from datetime import datetime



# Lista de tickers com 749 itens (exemplo)
tickers = ['AAPL', 'GOOGL', 'AMZN', 'MSFT'] * 187 + ['TSLA']  # Exemplo com 749 elementos


def tqdm_exemple():
    # Loop para buscar dados dos tickers com barra de progresso
    for ticker in tqdm(tickers, desc="Buscando dados dos tickers"):
        # Aqui vai sua função de pesquisa real
        # por exemplo: buscar_dados(ticker)
        time.sleep(0.1)  # simular tempo de pesquisa

# print("\ntqdm_exemplo()")
# tqdm_exemple()

def alive_progress_exemple():
    with alive_bar(len(tickers), title="Buscando dados dos tickers") as bar:
        for ticker in tickers:
            bar()
            time.sleep(0.1) # simular tempo de pesquisa

# print("\nalive_progress_exemple()")
# alive_progress_exemple()

def progressbar_exemple():
    bar = progressbar.ProgressBar(max_value=len(tickers))
    for i, ticker in enumerate(tickers):
        bar.update(i+1)
        time.sleep(0.1)

# print("\nprogressbar_exemple()")
# progressbar_exemple()

def rich_exemple():
    with Progress() as progress:
        task = progress.add_task("Buscando dados dos tickers", total=len(tickers))
        for ticker in tickers:
            progress.advance(task)
            time.sleep(0.1)

# print("\nrich_exemple()")
# rich_exemple()

def manual_progress_exemple():
    total = len(tickers)
    for i, ticker in enumerate(tickers):
        progress = (i+1)/total*100
        sys.stdout.write(f"\rBuscando dados: {progress:.2f}% completo")
        sys.stdout.flush()
        time.sleep(0.1)

# print("\nmanual_progress_exemple()")
# manual_progress_exemple()



def reader_and_writer():  
    data = {
        'date':''
    }
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    data_folder = 'data'
    json_file = os.path.join(data_folder, 'date_search.json')
    
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    
    if os.path.exists(json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)

    if data['date'] < current_date:
        data_to_save = {
            'date' : current_date
        }

        with open(json_file, 'w') as file:
            json.dump(data_to_save, file, indent=4)
    else: 
        print("Base de dados atualizada!")



reader_and_writer()