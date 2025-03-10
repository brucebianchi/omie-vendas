import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# Função para fazer a requisição à API e coletar os dados de vendas para Anselmo
def obter_vendas_anselmo(data_inicial, data_final):
    # Acessando as chaves secretas configuradas no Streamlit Secrets
    app_key = st.secrets["APP_KEY_ANSELMO"]
    app_secret = st.secrets["APP_SECRET_ANSELMO"]

    st.write(f"APP_KEY_ANSELMO: {app_key}")  # Para depuração, pode remover depois
    st.write(f"APP_SECRET_ANSELMO: {app_secret}")  # Para depuração, pode remover depois

    url = 'https://app.omie.com.br/api/v1/produtos/vendas-resumo/'
    headers = {'Content-Type': 'application/json'}
    body = {
        "call": "ObterResumoProdutos",
        "param": [
            {
                "dDataInicio": data_inicial,
                "dDataFim": data_final,
                "lApenasResumo": True
            }
        ],
        "app_key": app_key,
        "app_secret": app_secret
    }

    response = requests.post(url, json=body, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erro na requisição: {response.status_code}")
        return None

# Função para fazer a requisição à API e coletar os dados de vendas para Favinco
def obter_vendas_favinco(data_inicial, data_final):
    # Acessando as chaves secretas configuradas no Streamlit Secrets
    app_key = st.secrets["APP_KEY_FAVINCO"]
    app_secret = st.secrets["APP_SECRET_FAVINCO"]

    st.write(f"APP_KEY_FAVINCO: {app_key}")  # Para depuração, pode remover depois
    st.write(f"APP_SECRET_FAVINCO: {app_secret}")  # Para depuração, pode remover depois

    url = 'https://app.omie.com.br/api/v1/produtos/vendas-resumo/'
    headers = {'Content-Type': 'application/json'}
    body = {
        "call": "ObterResumoProdutos",
        "param": [
            {
                "dDataInicio": data_inicial,
                "dDataFim": data_final,
                "lApenasResumo": True
            }
        ],
        "app_key": app_key,
        "app_secret": app_secret
    }

    response = requests.post(url, json=body, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erro na requisição: {response.status_code}")
        return None

# Função para gerar o relatório diário de vendas
def gerar_relatorio_vendas(start_date, end_date):
    vendas_data = []
    total_acumulado = 0  # Variável para armazenar o valor acumulado
    current_date = start_date
    
    while current_date <= end_date:
        data_formatada = current_date.strftime('%d/%m/%Y')  # Formato brasileiro
        
        # Obter dados de vendas da Anselmo
        dados_anselmo = obter_vendas_anselmo(data_formatada, data_formatada)
        vendas_anselmo = dados_anselmo['pedidoVenda']['vFaturadas'] if dados_anselmo and 'pedidoVenda' in dados_anselmo else 0
        
        # Obter dados de vendas da Favinco
        dados_favinco = obter_vendas_favinco(data_formatada, data_formatada)
        vendas_favinco = dados_favinco['pedidoVenda']['vFaturadas'] if dados_favinco and 'pedidoVenda' in dados_favinco else 0
        
        # Somar as vendas de Anselmo e Favinco
        total_vendas = vendas_anselmo + vendas_favinco
        total_acumulado += total_vendas  # Atualiza o valor acumulado
        
        vendas_data.append({
            'Data': data_formatada,
            'Vendas Diárias - Anselmo': vendas_anselmo,
            'Vendas Diárias - Favinco': vendas_favinco,
            'Vendas Diárias - Total': total_vendas,
            'Acumulado Vendas': total_acumulado
        })
        
        current_date += timedelta(days=1)
    
    # Criar um DataFrame com os dados coletados
    df_vendas = pd.DataFrame(vendas_data)
    
    # Aplicando a formatação R$
    df_vendas['Vendas Diárias - Anselmo'] = df_vendas['Vendas Diárias - Anselmo'].apply(lambda x: f"R$ {x:,.2f}")
    df_vendas['Vendas Diárias - Favinco'] = df_vendas['Vendas Diárias - Favinco'].apply(lambda x: f"R$ {x:,.2f}")
    df_vendas['Vendas Diárias - Total'] = df_vendas['Vendas Diárias - Total'].apply(lambda x: f"R$ {x:,.2f}")
    df_vendas['Acumulado Vendas'] = df_vendas['Acumulado Vendas'].apply(lambda x: f"R$ {x:,.2f}")
    
    return df_vendas

# Streamlit app interface
st.title("Relatório de Vendas Diárias")

# Entrada de data
start_date = st.date_input("Data de Início", datetime(2025, 2, 1))
end_date = st.date_input("Data de Fim", datetime(2025, 2, 28))

# Adicionar opção para consultar a resposta da API
mostrar_resposta_api = st.checkbox("Mostrar resposta da API")

if st.button('Gerar Relatório'):
    df_vendas = gerar_relatorio_vendas(start_date, end_date)
    
    # Exibe o DataFrame com formatação
    st.markdown("<h3 style='color:orange;'>Relatório de Vendas Diárias</h3>", unsafe_allow_html=True)
    st.write(df_vendas.style.set_properties(subset=['Vendas Diárias - Anselmo', 'Vendas Diárias - Favinco', 'Vendas Diárias - Total', 'Acumulado Vendas'], 
                                            **{'text-align': 'right'}))  # Alinha as colunas à direita
    
    # Mostrar resposta da API se solicitado
    if mostrar_resposta_api:
        st.write("Resposta da API (Anselmo):")
        dados_anselmo = obter_vendas_anselmo(start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'))
        st.write(dados_anselmo)  # Exibe os dados da API para inspeção de Anselmo
        
        st.write("Resposta da API (Favinco):")
        dados_favinco = obter_vendas_favinco(start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'))
        st.write(dados_favinco)  # Exibe os dados da API para inspeção de Favinco
