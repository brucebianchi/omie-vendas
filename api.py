import requests

def obter_vendas_anselmo(data_inicial, data_final, app_key, app_secret):
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
        "app_key": app_key,
        "app_secret": app_secret
    }

    response = requests.post(url, json=body, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def obter_vendas_favinco(data_inicial, data_final, app_key, app_secret):
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
        "app_key": app_key,
        "app_secret": app_secret
    }

    response = requests.post(url, json=body, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Funções de pedidos e vendedores seriam similares, só mudando a URL e os parâmetros conforme necessário.

def obter_vendedores_unicos_e_vendas_anselmo(data_inicial, data_final, app_key, app_secret):
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
        "app_key": app_key,
        "app_secret": app_secret
    }

    response = requests.post(url, json=body, headers=headers)
    
    if response.status_code == 200:
        pedidos = response.json()
        
        vendedores = {}  # Usamos um dicionário para armazenar os dados dos vendedores e suas vendas
        if pedidos.get('pedido_venda_produto'):
            for pedido in pedidos['pedido_venda_produto']:
                if pedido.get('infoCadastro', {}).get('cancelado') == 'N':  # Verifica se o pedido não está cancelado
                    vendedor_id = pedido.get('informacoes_adicionais', {}).get('codVend')  # Acessa o campo 'codVend' para o vendedor
                    if vendedor_id:
                        valor_total = pedido.get('total_pedido', {}).get('valor_total_pedido', 0)  # Obtém o valor total do pedido
                        if vendedor_id not in vendedores:
                            vendedores[vendedor_id] = 0
                        vendedores[vendedor_id] += valor_total  # Acumula as vendas do vendedor
        return vendedores  # Retorna o dicionário de vendedores e suas vendas totais
    else:
        return None

def obter_vendedores_unicos_e_vendas_favinco(data_inicial, data_final, app_key, app_secret):
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
        "app_key": app_key,
        "app_secret": app_secret
    }

    response = requests.post(url, json=body, headers=headers)
    
    if response.status_code == 200:
        pedidos = response.json()
        
        vendedores = {}  # Usamos um dicionário para armazenar os dados dos vendedores e suas vendas
        if pedidos.get('pedido_venda_produto'):
            for pedido in pedidos['pedido_venda_produto']:
                if pedido.get('infoCadastro', {}).get('cancelado') == 'N':  # Verifica se o pedido não está cancelado
                    vendedor_id = pedido.get('informacoes_adicionais', {}).get('codVend')  # Acessa o campo 'codVend' para o vendedor
                    if vendedor_id:
                        valor_total = pedido.get('total_pedido', {}).get('valor_total_pedido', 0)  # Obtém o valor total do pedido
                        if vendedor_id not in vendedores:
                            vendedores[vendedor_id] = 0
                        vendedores[vendedor_id] += valor_total  # Acumula as vendas do vendedor
        return vendedores  # Retorna o dicionário de vendedores e suas vendas totais
    else:
        return None
