from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import csv

# Configurar Selenium
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

# Página inicial
driver.get("https://rostr.disney.com/people/4f642c7b2a27eb0da8f2490016c0808f?locale=en")

# Resultado da hierarquia
hierarquia = []

# Função para extrair informações do bloco "Company Info"
def extrair_company_info():
    campos = {
        "Company Code": "",
        "Business Area": "",
        "Personnel Area": "",
        "Organizational Unit": "",
        "Cost Center": "",
        "Employee Type": ""
    }

    try:
        cards = driver.find_elements(By.CLASS_NAME, "card")
        for card in cards:
            try:
                titulo = card.find_element(By.TAG_NAME, "h3").text.strip()
                if titulo == "Company Info":
                    dts = card.find_elements(By.TAG_NAME, "dt")
                    dds = card.find_elements(By.TAG_NAME, "dd")
                    for dt, dd in zip(dts, dds):
                        campo = dt.text.strip()
                        valor = dd.text.strip()
                        if campo in campos:
                            campos[campo] = valor
                    break
            except:
                continue
    except:
        pass

    return campos

# Função principal para visitar cada link
def visitar_pessoa_por_link(link, supervisor=None):
    try:
        driver.get(link)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "heading")))
        time.sleep(1)

        # Capturar supervisor real (se disponível)
        try:
            supervisor_name = driver.find_element(By.CSS_SELECTOR, "h4.heading").text.strip()
        except NoSuchElementException:
            supervisor_name = "SEM SUPERVISOR"

        # Extrair o nome da pessoa atual
        nome = driver.find_element(By.CSS_SELECTOR, "div.name-wrapper.hidden-xs.hidden-sm > h2").text.strip()
        print(f"Visitando: {nome} - Supervisor: {supervisor_name}")

        # Extrair informações da seção Company Info
        info = extrair_company_info()

        # Adicionar à hierarquia
        hierarquia.append([
            nome,
            supervisor_name,
            info["Company Code"],
            info["Business Area"],
            info["Personnel Area"],
            info["Organizational Unit"],
            info["Cost Center"],
            info["Employee Type"]
        ])

        # Buscar subordinados
        try:
            reports_ul = driver.find_element(By.CLASS_NAME, "reports")

            try:
                direct_div = reports_ul.find_element(By.CLASS_NAME, "direct-reports-peers")
                if direct_div.text.strip() == "":
                    return  # sem subordinados
            except:
                pass

            subordinados = reports_ul.find_elements(By.XPATH, ".//a")
            for sub_a in subordinados:
                sub_link = sub_a.get_attribute("href")
                visitar_pessoa_por_link(sub_link, supervisor=nome)

        except:
            pass  # folha da árvore

    except Exception as e:
        print(f"Erro ao visitar {link}: {e}")

# Função inicial: extrair todos os <a> do primeiro grupo
def iniciar():
    try:
        peers_ul = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "peers")))
        pessoas = peers_ul.find_elements(By.XPATH, ".//a")
        links = [p.get_attribute("href") for p in pessoas]
        for link in links:
            visitar_pessoa_por_link(link)
    except Exception as e:
        print(f"Erro ao iniciar extração: {e}")

# Iniciar processo
iniciar()

# Salvar CSV
with open("hierarquia.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Nome", "Supervisor",
        "Company Code", "Business Area",
        "Personnel Area", "Organizational Unit",
        "Cost Center", "Employee Type"
    ])
    writer.writerows(hierarquia)

print("✅ Extração concluída com sucesso!")

