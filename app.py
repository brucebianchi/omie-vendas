import base64
import streamlit as st
import requests
import pandas as pd
import json
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

# Função para obter vendedores únicos a partir dos pedidos de venda
def obter_vendedores_unicos(data_inicial, data_final):
    url = 'https://app.omie.com.br/api/v1/produtos/pedido/'
    headers = {'Content-Type': 'application/json'}
    body = {
        "call": "ListarPedidos",
        "param": [
            {
                "pagina": 1,
                "registros_por_pagina": 100,
                "apenas_importado_api": "N",
                "data_faturamento_de": data_inicial,
                "data_faturamento_ate": data_final
            }
        ],
        "app_key": app_key_anselmo,  # A chave codificada que estamos usando
        "app_secret": app_secret_anselmo  # O segredo codificado
    }

    response = requests.post(url, json=body, headers=headers)
    
    if response.status_code == 200:
        pedidos = response.json()
        
        vendedores = {}  # Usamos um dicionário para armazenar dados de cada vendedor
        
        if pedidos.get('pedido_venda_produto'):
            for pedido in pedidos['pedido_venda_produto']:
                vendedor_id = pedido.get('informacoes_adicionais', {}).get('codVend')  # Acessa o campo 'codVend' para o vendedor
                if vendedor_id:
                    valor_total = pedido.get('total_pedido', {}).get('valor_total_pedido', 0)  # Obtém o valor total do pedido
                    if vendedor_id not in vendedores:
                        vendedores[vendedor_id] = {'Anselmo': 0, 'Favinco': 0}
                    vendedores[vendedor_id]['Anselmo'] += valor_total  # Acumula as vendas de Anselmo
                    # Aqui você pode adicionar lógica para somar vendas de Favinco, se aplicável.
        return vendedores  # Retorna os vendedores com as vendas associadas
    else:
        st.error(f"Erro ao consultar vendedores: {response.status_code}")
        return None

# Função para gerar o relatório diário de vendas
def gerar_relatorio_vendas(start_date, end_date):
    vendas_data = []
    total_acumulado = 0  # Variável para armazenar o valor acumulado
    vendedores_info = []  # Lista para armazenar as informações dos vendedores
    current_date = start_date
    
    while current_date <= end_date:
        data_formatada = current_date.strftime('%d/%m/%Y')  # Formato brasileiro
        
        # Obter dados de vendas da Anselmo
        dados_anselmo = obter_vendas_anselmo(data_formatada, data_formatada)
        vendas_anselmo = dados_anselmo['pedidoVenda']['vFaturadas'] if dados_anselmo and 'pedidoVenda' in dados_anselmo else 0
        
        # Obter dados de vendedores únicos
        vendedores_unicos = obter_vendedores_unicos(data_formatada, data_formatada)
        
        # Somar as vendas de Anselmo
        total_vendas = vendas_anselmo
        total_acumulado += total_vendas  # Atualiza o valor acumulado
        
        vendas_data.append({
            'Data': data_formatada,
            'Vendas Diárias - Anselmo': vendas_anselmo,
            'Vendas Diárias - Total': total_vendas,
            'Acumulado Vendas': total_acumulado
        })
        
        # Adicionando os vendedores com vendas no dia
        for vendedor_id, vendas in vendedores_unicos.items():
            vendedores_info.append({
                'Data': data_formatada,
                'Vendedor': vendedor_id,
                'Vendas Anselmo': f"R$ {vendas['Anselmo']:,.2f}",
                'Vendas Favinco': f"R$ {vendas['Favinco']:,.2f}"  # Adiciona Favinco (se disponível)
            })
        
        current_date += timedelta(days=1)
    
    # Criar DataFrames
    df_vendas = pd.DataFrame(vendas_data)
    df_vendedores = pd.DataFrame(vendedores_info)
    
    # Aplicando a formatação R$
    df_vendas['Vendas Diárias - Anselmo'] = df_vendas['Vendas Diárias - Anselmo'].apply(lambda x: f"R$ {x:,.2f}")
    df_vendas['Vendas Diárias - Total'] = df_vendas['Vendas Diárias - Total'].apply(lambda x: f"R$ {x:,.2f}")
    df_vendas['Acumulado Vendas'] = df_vendas['Acumulado Vendas'].apply(lambda x: f"R$ {x:,.2f}")
    
    return df_vendas, df_vendedores

# Streamlit app interface
st.title("Relatório de Vendas Diárias")

# Entrada de data
start_date = st.date_input("Data de Início", datetime(2025, 2, 1))
end_date = st.date_input("Data de Fim", datetime(2025, 2, 28))

# Adicionar opção para consultar a resposta da API
mostrar_resposta_api = st.checkbox("Mostrar resposta da API")

if st.button('Gerar Relatório'):
    df_vendas, df_vendedores = gerar_relatorio_vendas(start_date, end_date)
    
    # Exibe o DataFrame de vendas com formatação
    st.markdown("<h3 style='color:orange;'>Relatório de Vendas Diárias</h3>", unsafe_allow_html=True)
    st.write(df_vendas.style.set_properties(subset=['Vendas Diárias - Anselmo', 'Vendas Diárias - Total', 'Acumulado Vendas'], 
                                            **{'text-align': 'right'}))  # Alinha as colunas à direita
    
    # Exibe o DataFrame de vendedores com vendas
    st.markdown("<h3 style='color:green;'>Vendedores com Vendas</h3>", unsafe_allow_html=True)
    st.write(df_vendedores)
    
    # Mostrar resposta da API se solicitado
    if mostrar_resposta_api:
        st.write("Resposta da API (Anselmo):")
        dados_anselmo = obter_vendas_anselmo(start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'))
        st.write(dados_anselmo)  # Exibe os dados da API para inspeção de Anselmo
        
        st.write("Vendedores com Vendas:")
        vendedores_unicos = obter_vendedores_unicos(start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'))
        st.write(vendedores_unicos)  # Exibe os vendedores únicos no período
