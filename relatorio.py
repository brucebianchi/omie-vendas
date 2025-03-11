import pandas as pd
from datetime import timedelta

def gerar_relatorio_vendas(start_date, end_date, 
                            obter_vendas_anselmo, obter_vendas_favinco,
                            app_key_anselmo, app_secret_anselmo,
                            app_key_favinco, app_secret_favinco):
    vendas_data = []
    total_acumulado = 0  # Variável para armazenar o valor acumulado
    current_date = start_date
    
    while current_date <= end_date:
        data_formatada = current_date.strftime('%d/%m/%Y')  # Formato brasileiro
        
        # Obter dados de vendas da Anselmo
        dados_anselmo = obter_vendas_anselmo(data_formatada, data_formatada, app_key_anselmo, app_secret_anselmo)
        vendas_anselmo = dados_anselmo['pedidoVenda']['vFaturadas'] if dados_anselmo and 'pedidoVenda' in dados_anselmo else 0
        
        # Obter dados de vendas da Favinco
        dados_favinco = obter_vendas_favinco(data_formatada, data_formatada, app_key_favinco, app_secret_favinco)
        vendas_favinco = dados_favinco['pedidoVenda']['vFaturadas'] if dados_favinco and 'pedidoVenda' in dados_favinco else 0
        
        # Somar as vendas de Anselmo e Favinco
        total_vendas = vendas_anselmo + vendas_favinco
        total_acumulado += total_vendas  # Atualiza o valor acumulado
        
        vendas_data.append({
            'Data': data_formatada,
            'Vendas Diárias - Anselmo': vendas_anselmo,
            'Vendas Diárias - Favinco': vendas_favinco,
            'Vendas Diárias - Total': total_vendas,
            'Acumulado Vendas': total_acumulado
        })
        
        current_date += timedelta(days=1)
    
    # Criar um DataFrame com os dados coletados
    df_vendas = pd.DataFrame(vendas_data)
    
    # Verificar se o DataFrame está vazio
    if df_vendas.empty:
        return pd.DataFrame(columns=["Data", "Vendas Diárias - Anselmo", "Vendas Diárias - Favinco", "Vendas Diárias - Total", "Acumulado Vendas"])

    # Formatar as colunas de valores para o padrão brasileiro (R$)
    df_vendas['Vendas Diárias - Anselmo'] = df_vendas['Vendas Diárias - Anselmo'].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    df_vendas['Vendas Diárias - Favinco'] = df_vendas['Vendas Diárias - Favinco'].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    df_vendas['Vendas Diárias - Total'] = df_vendas['Vendas Diárias - Total'].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    df_vendas['Acumulado Vendas'] = df_vendas['Acumulado Vendas'].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    # Ajustar o índice para começar de 1
    df_vendas.reset_index(drop=True, inplace=True)
    df_vendas.index += 1  # Começar a contagem do índice a partir de 1
    
    # Aplicar o alinhamento à direita nas colunas de valores
    df_vendas = df_vendas.style.set_properties(subset=['Vendas Diárias - Anselmo', 'Vendas Diárias - Favinco', 'Vendas Diárias - Total', 'Acumulado Vendas'], 
                                               **{'text-align': 'right'})
    
    return df_vendas

def gerar_relatorio_vendedores(start_date, end_date, 
                                obter_vendedores_anselmo, obter_vendedores_favinco,
                                app_key_anselmo, app_secret_anselmo,
                                app_key_favinco, app_secret_favinco,
                                obter_nome_vendedor):
    vendedores_info = []

    # Obter os vendedores únicos e suas vendas totais para Anselmo
    vendedores_unicos_anselmo = obter_vendedores_anselmo(start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'), app_key_anselmo, app_secret_anselmo)
    if not vendedores_unicos_anselmo:
        vendedores_unicos_anselmo = {}

    # Obter os vendedores únicos e suas vendas totais para Favinco
    vendedores_unicos_favinco = obter_vendedores_favinco(start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'), app_key_favinco, app_secret_favinco)
    if not vendedores_unicos_favinco:
        vendedores_unicos_favinco = {}

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
            'Vendas Anselmo': f"R$ {vendas['Vendas Anselmo']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
            'Vendas Favinco': f"R$ {vendas['Vendas Favinco']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
            'Total de Vendas': f"R$ {total_vendas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
            'Percentual de Contribuição': f"{percentual:,.2f}%".replace(',', 'X').replace('.', ',').replace('X', '.')
        })

    # Criar DataFrame com os dados dos vendedores
    df_vendedores = pd.DataFrame(vendedores_info)

    # Verificar se o DataFrame está vazio
    if df_vendedores.empty:
        return pd.DataFrame(columns=["Nome Vendedor", "Vendas Anselmo", "Vendas Favinco", "Total de Vendas", "Percentual de Contribuição"])

    # Alinhar à direita
    df_vendedores = df_vendedores.style.set_properties(subset=['Vendas Anselmo', 'Vendas Favinco', 'Total de Vendas', 'Percentual de Contribuição'], 
                                                       **{'text-align': 'right'})

    return df_vendedores
