# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv

# Configurar Selenium
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
driver.get("https://rostr.disney.com/people/4f642c7b2a27eb0da8f2490016c0808f?locale=en")

# Aguardar a página carregar completamente
time.sleep(20)

# Lista para armazenar (nome, supervisor)
hierarquia = []

def visitar_peers(peers_ul, supervisor=None):
    pessoas = peers_ul.find_elements(By.XPATH, "./li")
    
    for pessoa in pessoas:
        try:
            nome = pessoa.find_element(By.CLASS_NAME, "heading").text.strip()
        except:
            nome = "[SEM NOME]"
        
        print(f"{nome} - Supervisor: {supervisor}")
        hierarquia.append((nome, supervisor))
        
        # Verificar se tem <ul class="reports">
        try:
            reports_ul = pessoa.find_element(By.XPATH, ".//ul[contains(@class, 'reports')]")
            
            # Verifica se contém apenas um <div class="direct-reports-peers"> vazio
            try:
                direct = reports_ul.find_element(By.CLASS_NAME, "direct-reports-peers")
                if direct.text.strip() == "":
                    continue  # não há subordinados
            except:
                pass  # se não tiver div, assume que há subordinados

            # Recursão nos subordinados
            visitar_peers(reports_ul, supervisor=nome)

        except:
            continue  # sem reports

# Início: primeira <ul class="peers">
peers_iniciais = driver.find_element(By.CLASS_NAME, "peers")
visitar_peers(peers_iniciais)

# Salvar em CSV
with open("hierarquia.csv", "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Nome", "Supervisor"])
    writer.writerows(hierarquia)

print("Extração concluída!")
