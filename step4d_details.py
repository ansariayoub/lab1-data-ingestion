import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# ─── Charger la liste des produits ─────────────────────────────
with open("producthunt_products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

print(f"{len(products)} produits charges")

# ─── Construire les URLs depuis les IDs ────────────────────────
# Format URL ProductHunt : /posts/nom-du-produit
# On va construire l'URL depuis le nom
def nom_vers_slug(nom):
    import re
    slug = nom.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug.strip())
    return slug

# ─── Configurer Chrome ─────────────────────────────────────────
options = Options()
# Sans headless pour eviter le blocage de ProductHunt
options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
options.add_argument("--remote-allow-origins=*")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# ─── Scraper chaque page produit ───────────────────────────────
all_details = []

# On prend les 5 premiers pour ne pas surcharger
for i, produit in enumerate(products[:5]):
    nom = produit.get("name", "N/A")
    product_id = produit.get("id", "N/A")
    slug = nom_vers_slug(nom)
    url = f"https://www.producthunt.com/posts/{slug}"
    
    print(f"\nProduit {i+1}/5 : {nom}")
    print(f"URL : {url}")
    
    try:
        driver.get(url)
        time.sleep(5)
        
        # Scroll pour charger les reviews
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(2)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # ── Description detaillee ──────────────────────────────
        desc = "N/A"
        for tag in soup.find_all(["p", "div"]):
            texte = tag.get_text(strip=True)
            if len(texte) > 100 and len(texte) < 1000:
                desc = texte
                break
        
        # ── Rating ────────────────────────────────────────────
        rating = "N/A"
        rating_tag = soup.find(string=lambda t: t and "/5" in str(t))
        if rating_tag:
            rating = str(rating_tag).strip()
        
        # ── Nombre de reviews ─────────────────────────────────
        review_count = "N/A"
        review_tag = soup.find(string=lambda t: t and "review" in str(t).lower() and any(c.isdigit() for c in str(t)))
        if review_tag:
            review_count = str(review_tag).strip()
        
        # ── Topics / categories ───────────────────────────────
        topics = []
        topic_tags = soup.find_all("a", href=lambda x: x and "/topics/" in str(x))
        for t in topic_tags[:5]:
            txt = t.get_text(strip=True)
            if txt:
                topics.append(txt)
        
        # ── Website ───────────────────────────────────────────
        website = "N/A"
        for a in soup.find_all("a", href=True):
            href = a.get("href", "")
            if href.startswith("http") and "producthunt.com" not in href:
                website = href
                break
        
        detail = {
            "id":           product_id,
            "name":         nom,
            "tagline":      produit.get("tagline", "N/A"),
            "description":  desc[:200] if desc != "N/A" else "N/A",
            "rating":       rating,
            "review_count": review_count,
            "topics":       ", ".join(topics),
            "website":      website,
            "url_ph":       url
        }
        
        all_details.append(detail)
        print(f"  Rating    : {rating}")
        print(f"  Reviews   : {review_count}")
        print(f"  Topics    : {topics}")
        print(f"  Website   : {website}")
        
        # Sauvegarder progressivement
        with open("producthunt_details.json", "w", encoding="utf-8") as f:
            json.dump(all_details, f, ensure_ascii=False, indent=2)
        
        time.sleep(3)
        
    except Exception as e:
        print(f"  Erreur : {e}")
        continue

driver.quit()

# ─── Sauvegarder CSV final ─────────────────────────────────────
print(f"\nTotal : {len(all_details)} produits avec details")
df = pd.DataFrame(all_details)
print(df[["name", "rating", "review_count", "topics"]].to_string())
df.to_csv("producthunt_details.csv", index=False, encoding="utf-8")
print("\nCSV final sauvegarde : producthunt_details.csv")
print("Etape 4 terminee !")