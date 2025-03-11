import streamlit as st
from datetime import datetime
from api import obter_vendas_anselmo, obter_vendas_favinco, obter_vendedores_unicos_e_vendas_anselmo, obter_vendedores_unicos_e_vendas_favinco, obter_nome_vendedor
from relatorio import gerar_relatorio_vendas, gerar_relatorio_vendedores
from utils import decode_base64

# Decodificando as chaves
encoded_app_key_anselmo = "Mjg3NTA1ODQ1ODI3Mg=="
encoded_app_secret_anselmo = "NWQzYzY5NWUzYjJlZjZkYzFkZTU3YmU0ZDNlNzc0NGI="
app_key_anselmo = decode_base64(encoded_app_key_anselmo)
app_secret_anselmo = decode_base64(encoded_app_secret_anselmo)

encoded_app_key_favinco = "Mjg3NTAzNTQ1ODI5NQ=="
encoded_app_secret_favinco = "YTI1MmI5YTg5NjEyYmFiNGVhNjAzYWNmN2U1Zjc0ZWI="
app_key_favinco = decode_base64(encoded_app_key_favinco)
app_secret_favinco = decode_base64(encoded_app_secret_favinco)

st.title("Relatório de Vendas Diárias")

start_date = st.date_input("Data de Início", datetime(2025, 2, 1))
end_date = st.date_input("Data de Fim", datetime(2025, 2, 28))

# Checkbox para mostrar a resposta das APIs
mostrar_resposta_api = st.checkbox("Mostrar resposta da API")

if start_date > end_date:
    st.error("A data de início não pode ser maior que a data de fim.")
else:
    if st.button('Gerar Relatório'):
        df_vendas = gerar_relatorio_vendas(start_date, end_date, 
                                   obter_vendas_anselmo, 
                                   obter_vendas_favinco,
                                   app_key_anselmo, app_secret_anselmo,
                                   app_key_favinco, app_secret_favinco)

        st.markdown("<h3 style='color:orange;'>Relatório de Vendas Diárias</h3>", unsafe_allow_html=True)
        st.write(df_vendas)

                                        **{'text-align': 'right'}))

        df_vendedores = gerar_relatorio_vendedores(start_date, end_date, 
                                           obter_vendedores_unicos_e_vendas_anselmo,
                                           obter_vendedores_unicos_e_vendas_favinco,
                                           app_key_anselmo, app_secret_anselmo,
                                           app_key_favinco, app_secret_favinco,
                                           obter_nome_vendedor)

        st.markdown("<h3 style='color:green;'>Total de Vendas por Vendedor</h3>", unsafe_allow_html=True)
        st.write(df_vendedores)

        
        # Exibir resposta da API se a opção for selecionada
        if mostrar_resposta_api:
            st.write("Resposta da API (Anselmo):")
            dados_anselmo = obter_vendas_anselmo(start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'), app_key_anselmo, app_secret_anselmo)
            st.write(dados_anselmo)  # Exibe os dados da API para inspeção de Anselmo
            
            st.write("Resposta da API (Favinco):")
            dados_favinco = obter_vendas_favinco(start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'), app_key_favinco, app_secret_favinco)
            st.write(dados_favinco)  # Exibe os dados da API para inspeção de Favinco
