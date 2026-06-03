import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# ─── ETAPE 1 : Configuration Chrome ────────────────────────────
# REPONSE QUESTION LAB :
# SANS headless : Chrome s'ouvre visuellement → site le detecte moins
# AVEC headless : Chrome invisible → ProductHunt bloque completement !
options = Options()
# options.add_argument("--headless")  # COMMENTE car ProductHunt bloque headless
options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
options.add_argument("--remote-allow-origins=*")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# ─── ETAPE 2 : Lancer Chrome ───────────────────────────────────
print("Lancement du navigateur Chrome...")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# ─── ETAPE 3 : Naviguer vers ProductHunt ───────────────────────
url = "https://www.producthunt.com/search?q=mental+health+ai"
print(f"Ouverture : {url}")
driver.get(url)

# ─── ETAPE 4 : Attendre le chargement complet ──────────────────
print("Attente de 10 secondes (chargement JS complet)...")
time.sleep(10)

# ─── ETAPE 5 : Extraire via data-test (methode du collegue) ────
# ProductHunt met data-test="spotlight-result-product-XXXX" sur chaque produit
print("Recherche des produits via data-test...")

all_buttons = driver.find_elements(By.TAG_NAME, "button")
print(f"Nombre total de boutons trouves : {len(all_buttons)}")

products = []

for btn in all_buttons:
    data_test = btn.get_attribute("data-test")
    
    if data_test and "spotlight-result-product" in data_test:
        try:
            # Extraire le texte brut du bouton
            text_content = btn.text.strip().split("\n")
            print(f"  Contenu bouton : {text_content}")
            
            if len(text_content) >= 2:
                name    = text_content[0].strip()
                tagline = text_content[1].strip()
            elif len(text_content) == 1:
                name    = text_content[0].strip()
                tagline = "N/A"
            else:
                continue
            
            # Extraire l'ID depuis data-test
            product_id = data_test.split("-")[-1]
            
            # Chercher le lien vers la page produit
            try:
                lien_tag = btn.find_element(By.XPATH, ".//ancestor::a")
                lien = lien_tag.get_attribute("href")
            except:
                lien = "N/A"
            
            if name and len(name) > 1:
                products.append({
                    "id":      product_id,
                    "name":    name,
                    "tagline": tagline,
                    "url":     lien
                })
                print(f"Produit trouve : {name}")

        except Exception as e:
            print(f"  Erreur : {e}")
            continue

# ─── Si toujours 0, essayer avec les liens /posts/ ─────────────
if len(products) == 0:
    print("\nMethode boutons echouee, essai avec les liens /posts/...")
    
    try:
        # Attendre les liens produits
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/posts/')]"))
        )
    except:
        pass
    
    liens = driver.find_elements(By.XPATH, "//a[contains(@href, '/posts/')]")
    print(f"Liens /posts/ trouves : {len(liens)}")
    
    vus = set()
    for lien in liens:
        href = lien.get_attribute("href")
        if href and href not in vus and "/posts/" in href:
            vus.add(href)
            texte = lien.text.strip().split("\n")
            name    = texte[0] if texte else "N/A"
            tagline = texte[1] if len(texte) > 1 else "N/A"
            
            if name and len(name) > 2:
                product_id = href.split("/posts/")[-1].strip("/")
                products.append({
                    "id":      product_id,
                    "name":    name,
                    "tagline": tagline,
                    "url":     href
                })
                print(f"  Produit : {name}")

# ─── ETAPE 6 : Sauvegarder le HTML pour inspection ─────────────
with open("producthunt_raw.txt", "w", encoding="utf-8") as f:
    f.write(driver.page_source)
print("HTML sauvegarde dans producthunt_raw.txt")

driver.quit()
print("Navigateur ferme")

# ─── ETAPE 7 : Sauvegarder JSON et CSV ─────────────────────────
print(f"\nTotal : {len(products)} produits extraits")

if products:
    # JSON
    with open("producthunt_products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    print("JSON sauvegarde : producthunt_products.json")

    # CSV
    df = pd.DataFrame(products)
    print("\n=== APERCU ===")
    print(df)
    df.to_csv("producthunt_products.csv", index=False, encoding="utf-8")
    print("CSV sauvegarde : producthunt_products.csv")
    print("\nEtape 2 terminee avec succes !")

else:
    print("0 produits - affichage du HTML pour diagnostic...")
    with open("producthunt_raw.txt", "r", encoding="utf-8") as f:
        contenu = f.read()
    
    # Chercher indices dans le HTML
    print(f"Taille HTML : {len(contenu)} caracteres")
    print(f"Contient 'spotlight' : {'spotlight' in contenu}")
    print(f"Contient 'data-test' : {'data-test' in contenu}")
    print(f"Contient '/posts/' : {'/posts/' in contenu}")
    print(f"Contient 'mental' : {'mental' in contenu}")