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
        return response.json()
    else:
        st.error(f"Erro na requisição: {response.status_code}")
        return None

# Função para consultar o nome do vendedor pelo código
def obter_nome_vendedor(codigo_vendedor):
    url = 'https://app.omie.com.br/api/v1/geral/vendedores/'
    headers = {'Content-Type': 'application/json'}
    body = {
        "call": "ConsultarVendedor",
        "param": [
            {"codigo": codigo_vendedor}
        ],
        "app_key": app_key_anselmo,
        "app_secret": app_secret_anselmo
    }

    response = requests.post(url, json=body, headers=headers)
    
    if response.status_code == 200:
        dados_vendedor = response.json()
        if dados_vendedor and 'nome' in dados_vendedor[0]:
            return dados_vendedor[0]['nome']
        else:
            return "Desconhecido"
    else:
        st.error(f"Erro ao consultar o nome do vendedor: {response.status_code}")
        return "Desconhecido"

# Função para obter os vendedores únicos e somar as vendas totais de cada um para Anselmo
def obter_vendedores_unicos_e_vendas_anselmo(data_inicial, data_final):
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
        "app_key": app_key_anselmo,
        "app_secret": app_secret_anselmo
    }

    response = requests.post(url, json=body, headers=headers)
    
    if response.status_code == 200:
        pedidos = response.json()
        
        vendedores = {}  # Usamos um dicionário para armazenar os dados dos vendedores e suas vendas
        if pedidos.get('pedido_venda_produto'):
            for pedido in pedidos['pedido_venda_produto']:
                # Verifica se o pedido não está cancelado
                if pedido.get('infoCadastro', {}).get('cancelado') == 'N':
                    vendedor_id = pedido.get('informacoes_adicionais', {}).get('codVend')  # Acessa o campo 'codVend' para o vendedor
                    if vendedor_id:
                        valor_total = pedido.get('total_pedido', {}).get('valor_total_pedido', 0)  # Obtém o valor total do pedido
                        if vendedor_id not in vendedores:
                            vendedores[vendedor_id] = {'nome': "", 'vendas': 0}
                        vendedores[vendedor_id]['vendas'] += valor_total  # Acumula as vendas do vendedor
        return vendedores  # Retorna o dicionário de vendedores e suas vendas totais
    else:
        st.error(f"Erro ao consultar vendedores: {response.status_code}")
        return None

# Função para obter os vendedores únicos e somar as vendas totais de cada um para Favinco
def obter_vendedores_unicos_e_vendas_favinco(data_inicial, data_final):
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
        "app_key": app_key_favinco,
        "app_secret": app_secret_favinco
    }

    response = requests.post(url, json=body, headers=headers)
    
    if response.status_code == 200:
        pedidos = response.json()
        
        vendedores = {}  # Usamos um dicionário para armazenar os dados dos vendedores e suas vendas
        if pedidos.get('pedido_venda_produto'):
            for pedido in pedidos['pedido_venda_produto']:
                # Verifica se o pedido não está cancelado
                if pedido.get('infoCadastro', {}).get('cancelado') == 'N':
                    vendedor_id = pedido.get('informacoes_adicionais', {}).get('codVend')  # Acessa o campo 'codVend' para o vendedor
                    if vendedor_id:
                        valor_total = pedido.get('total_pedido', {}).get('valor_total_pedido', 0)  # Obtém o valor total do pedido
                        if vendedor_id not in vendedores:
                            vendedores[vendedor_id] = {'nome': "", 'vendas': 0}
                        vendedores[vendedor_id]['vendas'] += valor_total  # Acumula as vendas do vendedor
        return vendedores  # Retorna o dicionário de vendedores e suas vendas totais
    else:
        st.error(f"Erro ao consultar vendedores: {response.status_code}")
        return None

# Função para gerar o relatório de vendedores com suas vendas totais
def gerar_relatorio_vendedores(start_date, end_date):
    vendedores_info = []
    
    # Obter os vendedores únicos e suas vendas totais para Anselmo
    vendedores_unicos_anselmo = obter_vendedores_unicos_e_vendas_anselmo(start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'))
    
    # Obter os vendedores únicos e suas vendas totais para Favinco
    vendedores_unicos_favinco = obter_vendedores_unicos_e_vendas_favinco(start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'))
    
    # Unir os dados dos vendedores e somar as vendas
    for vendedor_id in set(vendedores_unicos_anselmo.keys()).union(vendedores_unicos_favinco.keys()):
        nome_anselmo = obter_nome_vendedor(vendedor_id)
        nome_favinco = obter_nome_vendedor(vendedor_id)
        total_vendas_anselmo = vendedores_unicos_anselmo.get(vendedor_id, {}).get('vendas', 0)
        total_vendas_favinco = vendedores_unicos_favinco.get(vendedor_id, {}).get('vendas', 0)
        
        vendedores_info.append({
            'Vendedor': nome_anselmo,  # Exibe o nome do vendedor
            'Vendas Anselmo': f"R$ {total_vendas_anselmo:,.2f}",
            'Vendas Favinco': f"R$ {total_vendas_favinco:,.2f}",
            'Total de Vendas': f"R$ {total_vendas_anselmo + total_vendas_favinco:,.2f}"
        })
    
    # Criar DataFrame com os dados dos vendedores
    df_vendedores = pd.DataFrame(vendedores_info)
    return df_vendedores

# Streamlit app interface
st.title("Relatório de Vendas Diárias")

# Entrada de data
start_date = st.date_input("Data de Início", datetime(2025, 2, 1))
end_date = st.date_input("Data de Fim", datetime(2025, 2, 28))

# Validação das datas
if start_date > end_date:
    st.error("A data de início não pode ser maior que a data de fim.")
else:
    mostrar_resposta_api = st.checkbox("Mostrar resposta da API")

    if st.button('Gerar Relatório'):
        # Gerar o relatório de vendas
        df_vendas = gerar_relatorio_vendas(start_date, end_date)
        
        # Exibe o DataFrame de vendas com formatação
        st.markdown("<h3 style='color:orange;'>Relatório de Vendas Diárias</h3>", unsafe_allow_html=True)
        st.write(df_vendas.style.set_properties(subset=['Vendas Diárias - Anselmo', 'Vendas Diárias - Favinco', 'Vendas Diárias - Total', 'Acumulado Vendas'], 
                                                **{'text-align': 'right'}))  # Alinha as colunas à direita
        
        # Gerar o relatório de vendedores
        df_vendedores = gerar_relatorio_vendedores(start_date, end_date)
        st.markdown("<h3 style='color:green;'>Total de Vendas por Vendedor</h3>", unsafe_allow_html=True)
        st.write(df_vendedores.style.set_properties(subset=['Total de Vendas'], **{'text-align': 'right'}))  # Alinha as colunas à direita
        
        # Mostrar resposta da API se solicitado
        if mostrar_resposta_api:
            st.write("Resposta da API (Anselmo):")
            dados_anselmo = obter_vendas_anselmo(start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'))
            st.write(dados_anselmo)  # Exibe os dados da API para inspeção de Anselmo
            
            st.write("Resposta da API (Favinco):")
            dados_favinco = obter_vendas_favinco(start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'))
            st.write(dados_favinco)  # Exibe os dados da API para inspeção de Favinco
