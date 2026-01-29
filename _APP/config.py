from datetime import datetime
from datetime import timedelta,date
import os

#Arquivo de configuração, que serve apenas para declarar variaveis que outros
#scripts vão usar

dias_semana = {
    0: "segunda-feira",
    1: "terça-feira",
    2: "quarta-feira",
    3: "quinta-feira",
    4: "sexta-feira",
    5: "sábado",
    6: "domingo"
}

dados_finais = {"Cidades": [],
                "Temperatura Máxima": [],
                "Temperatura Miníma": [],
                "Datas": []}

hoje = date.today()
dados_hoje = []
dados_futuros = []
cidade_extraida = ''
descrisao_clima = ''
data_hoje = ''
proximos_dias = [hoje + timedelta(days=i) for i in range(1, 9)]
nm_arquivo_API = "Previsão_tempo_API_openweathermap.csv"
nm_arquivo_webscaping = "Previsao_tempo_webscraping_g1.csv"

caminho_csv = os.path.join(os.path.dirname(__file__), "..", "_DOCS")
