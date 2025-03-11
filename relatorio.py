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
                                obter_vendedores_unicos_e_vendas_anselmo, 
                                obter_vendedores_unicos_e_vendas_favinco, 
                                app_key_anselmo, app_secret_anselmo, 
                                app_key_favinco, app_secret_favinco,
                                obter_nome_vendedor):
    
    # Obter vendedores e vendas de Anselmo
    vendedores_unicos_anselmo = obter_vendedores_unicos_e_vendas_anselmo(start_date, end_date, app_key_anselmo, app_secret_anselmo)
    if vendedores_unicos_anselmo is None:
        vendedores_unicos_anselmo = {}

    # Obter vendedores e vendas de Favinco
    vendedores_unicos_favinco = obter_vendedores_unicos_e_vendas_favinco(start_date, end_date, app_key_favinco, app_secret_favinco)
    if vendedores_unicos_favinco is None:
        vendedores_unicos_favinco = {}

    vendedores_completos = {}

    # Processar vendedores de Anselmo
    for vendedor_id in vendedores_unicos_anselmo:
        nome_vendedor = obter_nome_vendedor(vendedor_id, app_key_anselmo, app_secret_anselmo)
        if nome_vendedor:
            total_vendas_anselmo = vendedores_unicos_anselmo.get(vendedor_id, 0)
            vendedores_completos[vendedor_id] = {
                "Nome Vendedor": nome_vendedor,
                "Vendas Anselmo": total_vendas_anselmo,
                "Vendas Favinco": 0
            }

    # Processar vendedores de Favinco
    for vendedor_id in vendedores_unicos_favinco:
        nome_vendedor = obter_nome_vendedor(vendedor_id, app_key_favinco, app_secret_favinco)
        if nome_vendedor:
            total_vendas_favinco = vendedores_unicos_favinco.get(vendedor_id, 0)
            if vendedor_id in vendedores_completos:
                vendedores_completos[vendedor_id]["Vendas Favinco"] = total_vendas_favinco
            else:
                vendedores_completos[vendedor_id] = {
                    "Nome Vendedor": nome_vendedor,
                    "Vendas Anselmo": 0,
                    "Vendas Favinco": total_vendas_favinco
                }

    # Criar o DataFrame
    df_vendedores = pd.DataFrame.from_dict(vendedores_completos, orient="index")

    # Caso não haja dados, retornar um DataFrame vazio
    if df_vendedores.empty:
        return pd.DataFrame(columns=["Nome Vendedor", "Vendas Anselmo", "Vendas Favinco", "Total de Vendas", "Percentual de Contribuição"])

    # Calcular o total de vendas e o percentual de contribuição
    df_vendedores["Total de Vendas"] = df_vendedores["Vendas Anselmo"] + df_vendedores["Vendas Favinco"]
    total_vendas = df_vendedores["Total de Vendas"].sum()
    if total_vendas > 0:
        df_vendedores["Percentual de Contribuição"] = df_vendedores["Total de Vendas"] / total_vendas * 100
    else:
        df_vendedores["Percentual de Contribuição"] = 0

    # Retornar o DataFrame final
    return df_vendedores
