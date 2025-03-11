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
