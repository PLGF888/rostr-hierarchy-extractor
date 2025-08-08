from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import csv
from datetime import datetime
import inquirer
import sys
import re
import pretty_errors

pretty_errors.configure(
    separator_character = '─',
    filename_display    = pretty_errors.FILENAME_EXTENDED,
    line_number_first   = True,
    display_link        = True,
    lines_before        = 2,
    lines_after         = 2,
    truncate_code       = True,
    display_locals      = True
)

def validar_link(answers, current):
    if re.match(r'^https?://', current):
        return True
    return "Por favor, insira um link válido começando com http:// ou https://"

questions = [
    inquirer.Text('link', message="Insira o link da página inicial", validate=validar_link),
]

answers = inquirer.prompt(questions)

if not answers['link']:
    print("Pas de lien saisi. Execution annulee.")
    sys.exit(0)
print(answers['link'])

# Configurar Selenium
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)




# Página inicial
driver.get(answers['link'])
#driver.get("https://rostr.disney.com/people/270a898dd93f3a8d4a5bc73c9c5ea4c3?locale=en") #ASMAA
#driver.get("https://rostr.disney.com/people/018b65ccf17857ac5b0002e6f0f0f9ee?locale=en")  #Karine
#driver.get("https://rostr.disney.com/people/ea7b736f8ac180dc27b95c3bf8d5220c?locale=en")  #KENNY


# Resultado da hierarquia
hierarquia = []

visitados = set()  # <--- Conjunto para armazenar URLs já visitadas

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
    if link in visitados:
        return  # já visitado, evita loop
    visitados.add(link)
    
    try:
        driver.get(link)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "heading")))
        #time.sleep(1)

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
        
        # -----------------------------------TESTE INFO POSTE --------------------------------------- #
        try:
            p_tag = driver.find_element(By.CSS_SELECTOR, "p.text-center.visible-xs.visible-sm span")
            linhas = p_tag.get_attribute("innerHTML").split("<br>")
            cargo = linhas[0].strip().replace("<strong>", "").replace("</strong>", "") if len(linhas) > 0 else ""
            locacao = linhas[1].strip() if len(linhas) > 1 else ""
        except:
            cargo = ""
            locacao = ""
        
        
        
        
        # -----------------------------------TESTE INFO POSTE --------------------------------------- #

        # Adicionar à hierarquia
        hierarquia.append([
            nome,
            supervisor_name,
            cargo,
            locacao,
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
            sub_items = reports_ul.find_elements(By.TAG_NAME, "li")
            print(f"Subordinados: {len(sub_items)}")

            if len(sub_items) == 0:
                return  # não há subordinados

            sub_links = []            
            for li in sub_items:
                try:
                    sub_a = li.find_element(By.TAG_NAME, "a")
                    sub_links.append(sub_a.get_attribute("href"))
                    #visitar_pessoa_por_link(sub_link, supervisor=nome)
                except:
                    continue 
                
            for sub_link in sub_links:
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
with open(f"hierarquia_{datetime.today().strftime('%d-%m-%Y')}.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Nome", "Supervisor","Cargo","Locação",
        "Company Code", "Business Area",
        "Personnel Area", "Organizational Unit",
        "Cost Center", "Employee Type"
    ])
    writer.writerows(hierarquia)

print("✅ Extração concluída com sucesso!")

