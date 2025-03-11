import pandas as pd

def gerar_relatorio_vendas(start_date, end_date, obter_vendas_anselmo, obter_vendas_favinco):
    vendas_data = []
    total_acumulado = 0
    current_date = start_date
    
    while current_date <= end_date:
        data_formatada = current_date.strftime('%d/%m/%Y')
        dados_anselmo = obter_vendas_anselmo(data_formatada, data_formatada)
        vendas_anselmo = dados_anselmo['pedidoVenda']['vFaturadas'] if dados_anselmo else 0
        
        dados_favinco = obter_vendas_favinco(data_formatada, data_formatada)
        vendas_favinco = dados_favinco['pedidoVenda']['vFaturadas'] if dados_favinco else 0
        
        total_vendas = vendas_anselmo + vendas_favinco
        total_acumulado += total_vendas
        
        vendas_data.append({
            'Data': data_formatada,
            'Vendas Diárias - Anselmo': vendas_anselmo,
            'Vendas Diárias - Favinco': vendas_favinco,
            'Vendas Diárias - Total': total_vendas,
            'Acumulado Vendas': total_acumulado
        })
        
        current_date += timedelta(days=1)
    
    return pd.DataFrame(vendas_data)

# Função para gerar relatorio de vendedores...
