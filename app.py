import streamlit as st
from datetime import datetime
from api_requests import obter_vendas_anselmo, obter_vendas_favinco, obter_vendedores_unicos_e_vendas_anselmo, obter_vendedores_unicos_e_vendas_favinco
from utils import decode_base64
from reports import gerar_relatorio_vendas, gerar_relatorio_vendedores

# Carregar chaves codificadas
encoded_app_key_anselmo = "Mjg3NTA1ODQ1ODI3Mg=="
encoded_app_secret_anselmo = "NWQzYzY5NWUzYjJlZjZkYzFkZTU3YmU0ZDNlNzc0NGI="
encoded_app_key_favinco = "Mjg3NTAzNTQ1ODI5NQ=="
encoded_app_secret_favinco = "YTI1MmI5YTg5NjEyYmFiNGVhNjAzYWNmN2U1Zjc0ZWI="

app_key_anselmo = decode_base64(encoded_app_key_anselmo)
app_secret_anselmo = decode_base64(encoded_app_secret_anselmo)
app_key_favinco = decode_base64(encoded_app_key_favinco)
app_secret_favinco = decode_base64(encoded_app_secret_favinco)

# Interface Streamlit
st.title("Relatório de Vendas Diárias")

# Entrada de data
start_date = st.date_input("Data de Início", datetime(2025, 2, 1))
end_date = st.date_input("Data de Fim", datetime(2025, 2, 28))

if start_date > end_date:
    st.error("A data de início não pode ser maior que a data de fim.")
else:
    mostrar_resposta_api = st.checkbox("Mostrar resposta da API")

    if st.button('Gerar Relatório'):
        # Gerar o relatório de vendas, agora passando todas as credenciais
        df_vendas = gerar_relatorio_vendas(start_date, end_date, 
                                            obter_vendas_anselmo, obter_vendas_favinco,
                                            app_key_anselmo, app_secret_anselmo, 
                                            app_key_favinco, app_secret_favinco)
        
        st.markdown("<h3 style='color:orange;'>Relatório de Vendas Diárias</h3>", unsafe_allow_html=True)
        st.write(df_vendas)

        # Gerar o relatório de vendedores
        df_vendedores = gerar_relatorio_vendedores(start_date, end_date, 
                                                   obter_vendedores_unicos_e_vendas_anselmo, 
                                                   obter_vendedores_unicos_e_vendas_favinco,
                                                   app_key_anselmo, app_secret_anselmo, 
                                                   app_key_favinco, app_secret_favinco)
        
        st.markdown("<h3 style='color:green;'>Total de Vendas por Vendedor</h3>", unsafe_allow_html=True)
        st.write(df_vendedores)

        # Mostrar resposta da API se solicitado
        if mostrar_resposta_api:
            st.write("Resposta da API (Anselmo):")
            dados_anselmo = obter_vendas_anselmo(start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'), app_key_anselmo, app_secret_anselmo)
            st.write(dados_anselmo)
            
            st.write("Resposta da API (Favinco):")
            dados_favinco = obter_vendas_favinco(start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'), app_key_favinco, app_secret_favinco)
            st.write(dados_favinco)
