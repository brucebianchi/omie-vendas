import base64
import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# Função para decodificar a chave Base64
def decode_base64(encoded_str):
    decoded_bytes = base64.b64decode(encoded_str)
    return decoded_bytes.decode('utf-8')

# Função para codificar a chave em Base64 (apenas para gerar a chave codificada)
def encode_base64(original_str):
    return base64.b64encode(original_str.encode()).decode()

# Chaves codificadas em Base64
encoded_app_key_anselmo = "Mjg3NTA1ODQ1ODI3Mg=="  # Exemplo da chave codificada
encoded_app_secret_anselmo = "NWQzYzY5NWUzYjJlZjZkYzFkZTU3YmU0ZDNlNzc0NGI="  # Exemplo do segredo codificado

# Decodificando as chaves
app_key_anselmo = decode_base64(encoded_app_key_anselmo)
app_secret_anselmo = decode_base64(encoded_app_secret_anselmo)

# Função para fazer a requisição à API e coletar os dados de vendas para Anselmo
def obter_vendas_anselmo(data_inicial, data_final):
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
        "app_key": app_key_anselmo,
        "app_secret": app_secret_anselmo
    }

    response = requests.post(url, json=body, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erro na requisição: {response.status_code}")
        return None

# Função para fazer a requisição à API e coletar os dados de vendas para Favinco
def obter_vendas_favinco(data_inicial, data_final):
    # Chaves codificadas em Base64 para Favinco
    encoded_app_key_favinco = "Mjg3NTAzNTQ1ODI5NQ=="  # Exemplo da chave codificada
    encoded_app_secret_favinco = "YTI1MmI5YTg5NjEyYmFiNGVhNjAzYWNmN2U1Zjc0ZWI="  # Exemplo do segredo codificado
    
    # Decodificando as chaves
    app_key_favinco = decode_base64(encoded_app_key_favinco)
    app_secret_favinco = decode_base64(encoded_app_secret_favinco)

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
        "app_key": app_key_favinco,
        "app_secret": app_secret_favinco
    }

    response = requests.post(url, json=body, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erro na requisição: {response.status_code}")
        return None

# Função para obter vendas por vendedor
def obter_vendas_por_vendedor(vendedor_id, data_inicial, data_final):
    url = 'https://app.omie.com.br/api/v1/produtos/pedido/'
    headers = {'Content-Type': 'application/json'}
    body = {
        "pagina": 1,
        "registros_por_pagina": 100,
        "apenas_importado_api": "N",
        "filtrar_por_vendedor": vendedor_id,
        "data_faturamento_de": data_inicial,
        "data_faturamento_ate": data_final
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code == 200:
        pedidos = response.json()
        total_vendas = 0
        if pedidos.get('pedidoVenda'):
            total_vendas = sum(pedido['vFaturadas'] for pedido in pedidos['pedidoVenda'])
        return total_vendas
    else:
        st.error(f"Erro ao consultar vendas do vendedor {vendedor_id}: {response.status_code}")
        return 0

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

# Validação das datas
if start_date > end_date:
    st.error("A data de início não pode ser maior que a data de fim.")
else:
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

        # Adicionando a consulta para vendedores 2, 3 e 8
        vendedores = [2, 3, 8]
        vendas_vendedores = []
        for vendedor_id in vendedores:
            total_vendas_vendedor = obter_vendas_por_vendedor(str(vendedor_id), start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'))
            vendas_vendedores.append({
                'Vendedor': f"Vendedor {vendedor_id}",
                'Total de Vendas': f"R$ {total_vendas_vendedor:,.2f}"
            })
        
        df_vendedores = pd.DataFrame(vendas_vendedores)
        st.markdown("<h3 style='color:orange;'>Total de Vendas por Vendedor</h3>", unsafe_allow_html=True)
        st.write(df_vendedores.style.set_properties(subset=['Total de Vendas'], **{'text-align': 'right'}))  # Alinha as colunas à direita
