import logging
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

logging.basicConfig(filename='logs/logsSistem.log', encoding='utf-8', level=logging.DEBUG)

def streamlit_initializer():
    try:
        complete_df = pd.read_csv('data/yfinance_tickers_results.csv')
        processed_df = pd.read_csv('processedData/tickers_ordenados.csv')

        sidebar = st.sidebar
        sidebar.header('Selecione o DataFrame')

        opcoes = ['DataFrame processado', 'DataFrame completo']
        opcao_selecionada = sidebar.selectbox('Selecione um DataFrame:', opcoes)

        if opcao_selecionada == 'DataFrame processado':

            graficos = ['Selecione','Gráfico de linhas', 'Candlestick']
            selected_chart = sidebar.selectbox('Selecione o tipo de gráfico para exibir:', graficos)

            st.markdown("<h1 style='text-align: center;'>Tabela Tickers da B3</h1>", unsafe_allow_html=True)

            tickers = processed_df['Ticker'].unique()

            if selected_chart!='Selecione':

                selectedTicker = sidebar.selectbox('Selecione um dos ativos, para exibir os dados:',tickers[:10])

                df_filtrado = complete_df[complete_df['Ticker']==selectedTicker]
                datas = df_filtrado['Data'].unique()

                colunas=[]
                dados = []
                for data in datas:
                    colunas.append(data)

                for index, row in df_filtrado.iterrows():
                    dados.append(row['Close'])

                ticker_df_selecionado = pd.DataFrame([dados], columns=colunas)


            if selected_chart=='Gráfico de linhas':

                df = ticker_df_selecionado.T
                df.index = pd.to_datetime(df.index)
                # st.title('Gráfico de linhas', unsafe_allow_html=True)
                st.title('Gráfico de linhas')
                for coluna in df.columns:
                    st.line_chart(df[coluna])
                st.write(f'Valores de fechamento do ticker {selectedTicker} dos últimos 4 meses')
                st.dataframe(ticker_df_selecionado, use_container_width=True, hide_index=True)

            elif selected_chart=='Candlestick':
                fig = go.Figure(data=[go.Candlestick(
                                x=df_filtrado['Data'],
                                open=df_filtrado['Open'],
                                high=df_filtrado['High'],
                                low=df_filtrado['Low'],
                                close=df_filtrado['Close'])])

                tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
                with tab1:
                    st.plotly_chart(fig, theme="streamlit")
                with tab2:
                    st.plotly_chart(fig, theme=None)

                st.write(f"<h3 style='text-align: center;'>Dados de {selectedTicker}</h3>", unsafe_allow_html=True)
                st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

            st.write("<h3 style='text-align: center;'>Os 10 tickers da B3 mais rentáveis</h3>", unsafe_allow_html=True)
            st.write("<h5 style='text-align: center;'>(últimos 4 meses)</h5>", unsafe_allow_html=True)
            st.dataframe(processed_df.head(10), use_container_width=True, hide_index=True)

        elif opcao_selecionada == 'DataFrame completo':
            # st.title('Dados dos Tickers do índice Bovespa de 2024')
            st.markdown("<h1 style='text-align: center;'>Dados dos Tickers da B3</h1>", unsafe_allow_html=True)
            st.write("<h5 style='text-align: center;'>(últimos 4 meses)</h5>", unsafe_allow_html=True)


            tickers = complete_df['Ticker'].unique()

            selectedTicker = sidebar.selectbox('Escolha um Ativo:', tickers)
            df_filtrado = complete_df[complete_df['Ticker']==selectedTicker]

            st.write(f'Ticker selecionado: {selectedTicker}')

            fig = go.Figure(data=[go.Candlestick(
                            x=df_filtrado['Data'],
                            open=df_filtrado['Open'],
                            high=df_filtrado['High'],
                            low=df_filtrado['Low'],
                            close=df_filtrado['Close'])])

            tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
            with tab1:
                st.plotly_chart(fig, theme="streamlit")
            with tab2:
                st.plotly_chart(fig, theme=None)

            st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

        else:
            st.title('Nenhum DataFrame escolhido')
    except Exception as e:
        logging.warning(f'streamlit_arquive.streamlit_initializer(): {str(e)}')

streamlit_initializer()

