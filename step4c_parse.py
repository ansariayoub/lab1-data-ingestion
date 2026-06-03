import json
import pandas as pd

# ─── ETAPE 1 : Charger le JSON ─────────────────────────────────
print("Chargement du fichier JSON...")
with open("producthunt_products.json", "r", encoding="utf-8") as f:
    products = json.load(f)
print(f"{len(products)} produits charges")

# ─── ETAPE 2 : Nettoyer et structurer les donnees ──────────────
products_clean = []
for p in products:
    # Extraire le nombre de reviews depuis le tagline si present
    tagline = p.get("tagline", "N/A")
    reviews = "N/A"
    
    # Parfois le 3eme element contient "X reviews"
    if "review" in str(tagline).lower():
        reviews = tagline
        tagline = "N/A"
    
    products_clean.append({
        "id":       p.get("id", "N/A"),
        "name":     p.get("name", "N/A"),
        "tagline":  tagline,
        "reviews":  reviews,
        "url":      p.get("url", "N/A")
    })

# ─── ETAPE 3 : Creer le DataFrame ──────────────────────────────
df = pd.DataFrame(products_clean)

print("\n=== DONNEES FINALES ===")
print(df.to_string())
print(f"\nColonnes : {list(df.columns)}")
print(f"Nombre de produits : {len(df)}")

# ─── ETAPE 4 : Sauvegarder en CSV propre ───────────────────────
df.to_csv("producthunt_products.csv", index=False, encoding="utf-8")
print("\nCSV sauvegarde : producthunt_products.csv")
print("Etape 3 terminee !")