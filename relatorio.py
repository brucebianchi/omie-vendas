import pandas as pd
from datetime import timedelta

def gerar_relatorio_vendas(start_date, end_date, obter_vendas_anselmo, obter_vendas_favinco, app_key_anselmo, app_secret_anselmo, app_key_favinco, app_secret_favinco):
    vendas_data = []
    total_acumulado = 0  
    current_date = start_date
    
    while current_date <= end_date:
        data_formatada = current_date.strftime('%d/%m/%Y')  
        
        # Passar as chaves diretamente para as funções
        dados_anselmo = obter_vendas_anselmo(data_formatada, data_formatada, app_key_anselmo, app_secret_anselmo)
        vendas_anselmo = dados_anselmo['pedidoVenda']['vFaturadas'] if dados_anselmo and 'pedidoVenda' in dados_anselmo else 0
        
        dados_favinco = obter_vendas_favinco(data_formatada, data_formatada, app_key_favinco, app_secret_favinco)
        vendas_favinco = dados_favinco['pedidoVenda']['vFaturadas'] if dados_favinco and 'pedidoVenda' in dados_favinco else 0
        
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
    
    df_vendas = pd.DataFrame(vendas_data)
    df_vendas['Vendas Diárias - Anselmo'] = df_vendas['Vendas Diárias - Anselmo'].apply(lambda x: f"R$ {x:,.2f}")
    df_vendas['Vendas Diárias - Favinco'] = df_vendas['Vendas Diárias - Favinco'].apply(lambda x: f"R$ {x:,.2f}")
    df_vendas['Vendas Diárias - Total'] = df_vendas['Vendas Diárias - Total'].apply(lambda x: f"R$ {x:,.2f}")
    df_vendas['Acumulado Vendas'] = df_vendas['Acumulado Vendas'].apply(lambda x: f"R$ {x:,.2f}")
    
    return df_vendas

def gerar_relatorio_vendedores(start_date, end_date, 
                                obter_vendedores_anselmo, obter_vendedores_favinco,
                                app_key_anselmo, app_secret_anselmo,
                                app_key_favinco, app_secret_favinco,
                                obter_nome_vendedor):
    vendedores_info = []

    # Obter os vendedores únicos e suas vendas totais para Anselmo
    vendedores_unicos_anselmo = obter_vendedores_anselmo(start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'), app_key_anselmo, app_secret_anselmo)

    # Obter os vendedores únicos e suas vendas totais para Favinco
    vendedores_unicos_favinco = obter_vendedores_favinco(start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'), app_key_favinco, app_secret_favinco)

    # Unir os dados dos vendedores e somar as vendas
    for vendedor_id in set(vendedores_unicos_anselmo.keys()).union(vendedores_unicos_favinco.keys()):
        total_vendas_anselmo = vendedores_unicos_anselmo.get(vendedor_id, 0)
        total_vendas_favinco = vendedores_unicos_favinco.get(vendedor_id, 0)

        # Obter o nome do vendedor
        nome_vendedor_anselmo = obter_nome_vendedor(vendedor_id, app_key_anselmo, app_secret_anselmo)
        nome_vendedor_favinco = obter_nome_vendedor(vendedor_id, app_key_favinco, app_secret_favinco)

        vendedores_info.append({
            'Vendedor': vendedor_id,
            'Nome Anselmo': nome_vendedor_anselmo,
            'Nome Favinco': nome_vendedor_favinco,
            'Vendas Anselmo': f"R$ {total_vendas_anselmo:,.2f}",
            'Vendas Favinco': f"R$ {total_vendas_favinco:,.2f}",
            'Total de Vendas': f"R$ {total_vendas_anselmo + total_vendas_favinco:,.2f}"
        })

    # Criar DataFrame com os dados dos vendedores
    df_vendedores = pd.DataFrame(vendedores_info)
    return df_vendedores


