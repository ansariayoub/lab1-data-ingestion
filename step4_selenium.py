from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

# ─── Configuration du navigateur ───────────────────────────────
# Options du navigateur Chrome
options = Options()

# MODE HEADLESS = navigateur invisible (sans interface graphique)
# Commente cette ligne pour voir le navigateur s'ouvrir
options.add_argument("--headless")

# Options recommandées pour éviter les blocages
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36")

# ─── Lancer le navigateur ──────────────────────────────────────
# webdriver-manager télécharge automatiquement le bon driver Chrome
print("Lancement du navigateur...")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# ─── Naviguer vers ProductHunt ─────────────────────────────────
url = "https://www.producthunt.com/search?q=mental+health+ai"
print(f"Navigation vers : {url}")
driver.get(url)

# Attendre que la page charge complètement
# Nécessaire car JavaScript charge le contenu après la page
print("Attente chargement de la page (5 secondes)...")
time.sleep(5)

# ─── Sauvegarder le HTML de la page ────────────────────────────
page_source = driver.page_source
with open("producthunt_raw.txt", "w", encoding="utf-8") as f:
    f.write(page_source)
print("HTML sauvegardé dans producthunt_raw.txt")

# ─── Fermer le navigateur (bonne pratique) ─────────────────────
driver.quit()
print("Navigateur fermé")
print("Etape 1 terminée !")