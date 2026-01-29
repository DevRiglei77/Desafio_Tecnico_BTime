import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from utils import *


cidade,sigla = consulta_cidades()
nm_arquivo = "Previsao_tempo_webscraping_g1.csv"
driver = webdriver.Chrome()
driver.get("https://g1.globo.com/previsao-do-tempo/")


def extrai_texto_de_tag(metodo,indentificador,lista):
    resultado = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((eval(metodo), indentificador))
    )
    lista.extend(resultado.text.split("\n"))

#Se elemento ainda estiver visivel, significa que a cidade não foi encontrada
def verifica_existencia_elemento_busca(elemento_busca):

    try:
        if elemento_busca.is_displayed():
            cidade, sigla = consulta_cidades()
            elemento_busca.clear()
            consulta_clima_hoje()

    except Exception as E:
        return False

#Verifica se a pagina retornou um 404 ao tentar procurar uma cidade
def verifica_erro_404_busca():

    try:
        if driver.find_element(By.CLASS_NAME,"endereco-404").is_displayed():
            cidade, sigla = consulta_cidades()
            driver.back()
            time.sleep(2)
            consulta_clima_hoje()

    except Exception as E:
        return False

def consulta_clima_dos_proximos_sete_dias():
    extrai_texto_de_tag("By.CLASS_NAME", "forecast-next-days__content",dados_futuros)
    trata_dados_clima_dos_proximos_sete_dias()

#Função que extrai dados do clima de uma cidade na data de hoje
def consulta_clima_hoje():

    try:
         elemento_busca = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.NAME, "busca"))
        )
         elemento_busca.send_keys(cidade)
         time.sleep(2)
         elemento_busca.send_keys(Keys.ARROW_DOWN)
         elemento_busca.send_keys(Keys.ENTER)

         if not verifica_erro_404_busca() and not verifica_existencia_elemento_busca(elemento_busca):
             extrai_texto_de_tag("By.CLASS_NAME", 'forecast-header', dados_hoje)
             extrai_texto_de_tag("By.XPATH", "/html/body/div[2]/div[2]/div[1]/div[2]/div[4]/div[1]", dados_hoje)
             extrai_texto_de_tag("By.XPATH", "/html/body/div[2]/div[2]/div[1]/div[2]/div[4]/div[2]", dados_hoje)
             trata_dados_clima_hoje()
             consulta_clima_dos_proximos_sete_dias()


    except Exception as e:
        raise e



