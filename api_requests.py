import requests

def obter_vendas_anselmo(data_inicial, data_final, app_key, app_secret):
    url = 'https://app.omie.com.br/api/v1/produtos/vendas-resumo/'
    headers = {'Content-Type': 'application/json'}
    body = {
        "call": "ObterResumoProdutos",
        "param": [{"dDataInicio": data_inicial, "dDataFim": data_final, "lApenasResumo": True}],
        "app_key": app_key,
        "app_secret": app_secret
    }
    response = requests.post(url, json=body, headers=headers)
    return response.json() if response.status_code == 200 else None

def obter_vendas_favinco(data_inicial, data_final, app_key, app_secret):
    url = 'https://app.omie.com.br/api/v1/produtos/vendas-resumo/'
    headers = {'Content-Type': 'application/json'}
    body = {
        "call": "ObterResumoProdutos",
        "param": [{"dDataInicio": data_inicial, "dDataFim": data_final, "lApenasResumo": True}],
        "app_key": app_key,
        "app_secret": app_secret
    }
    response = requests.post(url, json=body, headers=headers)
    return response.json() if response.status_code == 200 else None

# Funções de vendedores...
