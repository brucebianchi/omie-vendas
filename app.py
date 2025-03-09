import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# Função para fazer a requisição à API e coletar os dados de vendas
def obter_vendas_data(data_inicial, data_final):
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
        "app_key": '2875058458272', 
        "app_secret": '5d3c695e3b2ef6dc1de57be4d3e7744b'
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
        dados = obter_vendas_data(data_formatada, data_formatada)
        
        if dados and 'pedidoVenda' in dados:  # A chave foi alterada para 'pedidoVenda'
            pedido_venda = dados['pedidoVenda']
            if 'vFaturadas' in pedido_venda:  # Acessa 'vFaturadas' dentro de 'pedidoVenda'
                valor_vendas = pedido_venda.get('vFaturadas', 0)
                total_acumulado += valor_vendas  # Atualiza o valor acumulado
                vendas_data.append({
                    'Data': data_formatada,
                    'Vendas no dia': valor_vendas,
                    'Vendas Acumuladas': total_acumulado
                })
        
        current_date += timedelta(days=1)
    
    # Criar um DataFrame com os dados coletados
    df_vendas = pd.DataFrame(vendas_data)
    
    # Aplicando a formatação R$
    df_vendas['Vendas no dia'] = df_vendas['Vendas no dia'].apply(lambda x: f"R$ {x:,.2f}")
    df_vendas['Vendas Acumuladas'] = df_vendas['Vendas Acumuladas'].apply(lambda x: f"R$ {x:,.2f}")
    
    return df_vendas

# Streamlit app interface
st.title("Relatório de Vendas Diárias")
start_date = st.date_input("Data de Início", datetime(2025, 2, 1))
end_date = st.date_input("Data de Fim", datetime(2025, 2, 28))

# Adicionar opção para consultar a resposta da API
mostrar_resposta_api = st.checkbox("Mostrar resposta da API")

if st.button('Gerar Relatório'):
    df_vendas = gerar_relatorio_vendas(start_date, end_date)
    
    # Exibe o DataFrame com formatação
    st.markdown("<h3 style='color:orange;'>Relatório de Vendas Diárias</h3>", unsafe_allow_html=True)
    st.write(df_vendas.style.set_properties(subset=['Vendas no dia', 'Vendas Acumuladas'], 
                                            **{'text-align': 'right'}))  # Alinha as colunas à direita
    
    # Mostrar resposta da API se solicitado
    if mostrar_resposta_api:
        st.write("Resposta da API:")
        dados = obter_vendas_data(start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'))
        st.write(dados)  # Exibe os dados da API para inspeção
