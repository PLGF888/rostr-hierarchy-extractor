from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import json
import time

# Configuração do Chrome
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

# Função principal
def extrair_info_pessoa(url, profundidade=0, urls_visitadas=None):
    if urls_visitadas is None:
        urls_visitadas = set()

    indent = "  " * profundidade
    driver.get(url)

    print(f"{indent}🔎 Visitando: {url}")
    time.sleep(1)

    # Nome da pessoa
    try:
        nome_elem = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.name-wrapper.hidden-xs.hidden-sm h2")))
        nome = nome_elem.text.strip()
    except TimeoutException:
        nome = "NOME NÃO ENCONTRADO"

    # Nome do supervisor
    try:
        supervisor = driver.find_element(By.CSS_SELECTOR, "h4.heading").text.strip()
    except NoSuchElementException:
        supervisor = "SEM SUPERVISOR"

    print(f"{indent}👤 Nome: {nome}")
    print(f"{indent}🧑‍💼 Supervisor: {supervisor}")

    dados = {
        "nome": nome,
        "supervisor": supervisor,
        "subordinados": []
    }

    # Verificar se a pessoa tem subordinados reais
    try:
        reports_ul = driver.find_element(By.CLASS_NAME, "reports")

        # Se tiver um div vazio de direct-reports-peers, não tem subordinados
        try:
            direct_div = reports_ul.find_element(By.CLASS_NAME, "direct-reports-peers")
            if direct_div.text.strip() == "":
                print(f"{indent}⚠️ Sem subordinados reais.")
                return dados
        except NoSuchElementException:
            # Sem esse div, assume que há subordinados
            pass

        # Para cada subordinado, visitar o link
        subordinados = reports_ul.find_elements(By.XPATH, ".//a")
        for sub_a in subordinados:
            sub_link = sub_a.get_attribute("href")
            if sub_link and sub_link not in urls_visitadas:
                urls_visitadas.add(sub_link)
                time.sleep(1)
                sub_info = extrair_info_pessoa(sub_link, profundidade + 1, urls_visitadas)
                dados["subordinados"].append(sub_info)

    except NoSuchElementException:
        print(f"{indent}⚠️ Nenhuma <ul class='reports'> encontrada.")

    return dados

# ======= EXECUÇÃO ========
url_inicial = "https://rostr.disney.com/people/b94e376c8e9305a1c0810cb110d62d52?locale=en"  # Substitua pela URL inicial da árvore

driver.get(url_inicial)
dados = extrair_info_pessoa(url_inicial)

driver.quit()

# Mostrar resultado
print("\n🗂️ Hierarquia extraída:")
print(json.dumps(dados, indent=2, ensure_ascii=False))
