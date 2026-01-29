import requests
import os
from dotenv import load_dotenv
from utils import sorteia_cidades,consulta_cidades,salva_dados,extrai_temperaturas_datas_api
import json


load_dotenv()
API_KEY = os.getenv('API_KEY_OPENWEATHERMAP')
cidade,sigla = consulta_cidades()


url = f"https://api.openweathermap.org/data/2.5/forecast?q={cidade}&appid={API_KEY}&lang=pt_br&cnt=16"

#Essa Api retorna a previsão dos tempos de alguns dias em diferentes horarios
def consulta_clima():

    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = json.loads(resposta.text)
        extrai_temperaturas_datas_api(dados,sigla)
    else:
        print("Falha na requisição:", resposta.status_code)
        exit()







