import  requests
import json
import random
import re
import csv
import locale
import os
from config import *

#Pega o nome da cidade e sigla da cidade sorteada
def trata_amostra(amostras):
    for amostra in amostras:
        cidade = amostra['microrregiao']['nome']
        sigla =  amostra['microrregiao']['mesorregiao']['UF']['sigla']
        return cidade,sigla

#Pega uma amostra dos dados de retorno da API do IBGE
def sorteia_cidades(lista_cidades):
    amostras = random.sample(lista_cidades, 1)
    return trata_amostra(amostras)

#Função que busca nomes de cidade na api do IBGE
def consulta_cidades():

    url = "https://servicodados.ibge.gov.br/api/v1/localidades/regioes/3/municipios"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = json.loads(resposta.text)
        return sorteia_cidades(dados)
    else:
        print("Falha na requisição:", resposta.status_code)

#Pega as temperaturas maximas e minimas do dia vigente atraves da
# lógica do maior e menor e tambem trata as datas
def trata_dados_clima_hoje():
    cidade_extraida = dados_hoje[1]
    temperatura_maxima = re.findall(r'(\d+)º', dados_hoje[3])
    temperatura_minima = re.findall(r'(\d+)º', dados_hoje[-1])
    temperatura_maxima = max(temperatura_maxima)
    temperatura_minima = min(temperatura_minima)
    data_hoje = dados_hoje[0] + "," + str(hoje.strftime('%d/%m/%Y'))
    dados_finais['Cidades'].append(cidade_extraida)
    dados_finais['Temperatura Máxima'].append(temperatura_maxima + "º" + "C")
    dados_finais['Temperatura Miníma'].append(temperatura_minima + "º" + "C")
    dados_finais['Datas'].append(data_hoje)

#Pega as temperaturas maximas e minimas dos proximos sete dias atraves da
# lógica do maior e menor e tambem trata as datas
def trata_dados_clima_dos_proximos_sete_dias():

    dados_futuros.pop()
    for indice,dado in enumerate(dados_futuros):
        temperaturas = re.findall(r'(\d+)º', dado)
        temperatura_maxima = max(temperaturas)
        temperatura_minima = min(temperaturas)
        datas = re.findall(r'[^0-9/*]*-*',dado,re.IGNORECASE)
        dia_semana = datas[0].strip()
        data = dia_semana + "," + str(proximos_dias[indice].strftime('%d/%m/%Y'))
        dados_finais['Cidades'].append(dados_hoje[1])
        dados_finais['Temperatura Máxima'].append(temperatura_maxima + "º" + "C")
        dados_finais['Temperatura Miníma'].append(temperatura_minima + "º" + "C")
        dados_finais['Datas'].append(data)
    salva_dados(nm_arquivo_webscaping)

def converte_escala_kelvin_p_escala_celsius(temperatura):
    temperatura = temperatura - 273.15
    return round(temperatura)

def trata_datas(data):
    data_hora = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
    return dias_semana[data_hora.weekday()].capitalize() + "," + data

def extrai_temperaturas_datas_api(dados,sigla):
    for valor in dados['list']:
        temperatura_maxima = converte_escala_kelvin_p_escala_celsius(valor['main']['temp_max'])
        temperatura_minima = converte_escala_kelvin_p_escala_celsius(valor['main']['temp_min'])
        data = trata_datas(valor['dt_txt'])
        cidade = dados['city']['name'] + "," + sigla
        guarda_dados_normalizados_api(temperatura_maxima,temperatura_minima,data,cidade)

    salva_dados(nm_arquivo_API)


def guarda_dados_normalizados_api(temperatura_maxima,temperatura_minima,data,cidade):
    dados_finais['Cidades'].append(cidade)
    dados_finais['Temperatura Máxima'].append(str(temperatura_maxima) + "º" + "C")
    dados_finais['Temperatura Miníma'].append(str(temperatura_minima) + "º" + "C")
    dados_finais['Datas'].append(data)


def esvazia_lista():
    dados_finais['Cidades'].clear()
    dados_finais['Temperatura Miníma'].clear()
    dados_finais['Temperatura Máxima'].clear()
    dados_finais['Datas'].clear()


#Função que salva os dados em um csv, é preciso
# passar como parametro o nome do arquivo
def salva_dados(nm_arquivo):

    cabecalhos = dados_finais.keys()
    caminho_completo = os.path.join(caminho_csv, nm_arquivo)
    with open(caminho_completo, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")

        # escreve cabeçalho
        writer.writerow(cabecalhos)

        # escreve linhas
        for i in range(len(next(iter(dados_finais.values())))):
            linha = [dados_finais[col][i] for col in cabecalhos]
            writer.writerow(linha)
    esvazia_lista()


