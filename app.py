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

    current_date = start_date
    while current_date <= end_date:
        data_formatada = current_date.strftime('%d/%m/%Y')
        dados = obter_vendas_data(data_formatada, data_formatada)
        
        if dados:
            # Verifica se a chave 'vendas' está presente na resposta
            if 'vendas' in dados:
                for item in dados['vendas']:
                    vendas_data.append({
                        'Data': data_formatada,
                        'Valor das Vendas (Anselmo)': item.get('vFaturadas', 0)  # Usando 'vFaturadas' que é o valor de Anselmo
                    })
            else:
                st.warning(f"Nenhuma venda encontrada para a data {data_formatada}")
        
        current_date += timedelta(days=1)
    
    # Criar um DataFrame com os dados coletados
    df_vendas = pd.DataFrame(vendas_data)
    
    # Gerar relatório com as colunas de 'Data' e 'Valor das Vendas'
    st.write(df_vendas)

    # Salvar os dados em um arquivo Excel
    nome_arquivo = f"relatorio_vendas_{start_date.strftime('%d%m%Y')}_{end_date.strftime('%d%m%Y')}.xlsx"
    df_vendas.to_excel(nome_arquivo, index=False, engine='openpyxl')

    # Fornecer um botão para download
    st.download_button(
        label="Baixar relatório em Excel",
        data=df_vendas.to_excel(index=False, engine='openpyxl'),
        file_name=nome_arquivo,
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# Streamlit app interface
st.title("Relatório de Vendas Diárias")
start_date = st.date_input("Data de Início", datetime(2025, 2, 1))
end_date = st.date_input("Data de Fim", datetime(2025, 2, 28))

if st.button('Gerar Relatório'):
    gerar_relatorio_vendas(start_date, end_date)
