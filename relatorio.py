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
    vendedores_completos = {}

    # Processar vendas de Anselmo
    for vendedor_id in vendedores_unicos_anselmo:
        nome_vendedor = obter_nome_vendedor(vendedor_id, app_key_anselmo, app_secret_anselmo)
        if nome_vendedor:
            total_vendas_anselmo = vendedores_unicos_anselmo.get(vendedor_id, 0)
            if nome_vendedor not in vendedores_completos:
                vendedores_completos[nome_vendedor] = {'Vendas Anselmo': total_vendas_anselmo, 'Vendas Favinco': 0}
            else:
                vendedores_completos[nome_vendedor]['Vendas Anselmo'] += total_vendas_anselmo

    # Processar vendas de Favinco
    for vendedor_id in vendedores_unicos_favinco:
        nome_vendedor = obter_nome_vendedor(vendedor_id, app_key_favinco, app_secret_favinco)
        if nome_vendedor:
            total_vendas_favinco = vendedores_unicos_favinco.get(vendedor_id, 0)
            if nome_vendedor not in vendedores_completos:
                vendedores_completos[nome_vendedor] = {'Vendas Anselmo': 0, 'Vendas Favinco': total_vendas_favinco}
            else:
                vendedores_completos[nome_vendedor]['Vendas Favinco'] += total_vendas_favinco

    # Calcular o total de vendas de todos os vendedores
    total_vendas_geral = sum([vendas['Vendas Anselmo'] + vendas['Vendas Favinco'] for vendas in vendedores_completos.values()])

    # Criar a lista de informações para os vendedores
    for nome, vendas in vendedores_completos.items():
        total_vendas = vendas['Vendas Anselmo'] + vendas['Vendas Favinco']
        percentual = (total_vendas / total_vendas_geral) * 100 if total_vendas_geral > 0 else 0

        vendedores_info.append({
            'Nome Vendedor': nome,
            'Vendas Anselmo': f"R$ {vendas['Vendas Anselmo']:,.2f}",
            'Vendas Favinco': f"R$ {vendas['Vendas Favinco']:,.2f}",
            'Total de Vendas': f"R$ {total_vendas:,.2f}",
            'Percentual de Contribuição': f"{percentual:,.2f}%"  # Formatação do percentual
        })

    # Criar DataFrame com os dados dos vendedores
    df_vendedores = pd.DataFrame(vendedores_info)
    return df_vendedores
