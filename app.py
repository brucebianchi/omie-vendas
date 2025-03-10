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

encoded_app_key_favinco = "Mjg3NTAzNTQ1ODI5NQ=="  # Exemplo da chave codificada
encoded_app_secret_favinco = "YTI1MmI5YTg5NjEyYmFiNGVhNjAzYWNmN2U1Zjc0ZWI="  # Exemplo do segredo codificado

# Decodificando as chaves
app_key_anselmo = decode_base64(encoded_app_key_anselmo)
app_secret_anselmo = decode_base64(encoded_app_secret_anselmo)

app_key_favinco = decode_base64(encoded_app_key_favinco)
app_secret_favinco = decode_base64(encoded_app_secret_favinco)

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
   
