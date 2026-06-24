from google_play_scraper import search, app, reviews, Sort
import json
import pandas as pd

# ─── ETAPE 1 : Rechercher des apps ─────────────────────────────
# La fonction search() cherche des apps par mot-cle
print("Recherche d'apps sur Google Play...")

resultats = search(
    "mental health ai",      # Mot-cle de recherche
    lang="en",               # Langue
    country="us",            # Pays
    n_hits=30                # Nombre de resultats voulus
)

print(f"{len(resultats)} apps trouvees")

# ─── ETAPE 2 : Extraire les donnees de chaque app ──────────────
apps_data = []

for r in resultats:
    apps_data.append({
        "app_id":       r.get("appId", "N/A"),
        "title":        r.get("title", "N/A"),
        "developer":    r.get("developer", "N/A"),
        "score":        r.get("score", 0),
        "ratings":      r.get("ratings", 0),
        "installs":     r.get("installs", "N/A"),
        "free":         r.get("free", True),
        "price":        r.get("price", 0),
        "genre":        r.get("genre", "N/A"),
        "description":  r.get("description", "N/A")[:200],
        "url":          r.get("url", "N/A")
    })
    print(f"  - {r.get('title')} | Score: {r.get('score')} | {r.get('installs')} installs")

# ─── ETAPE 3 : Sauvegarder les apps en JSON ────────────────────
with open("googleplay_apps.json", "w", encoding="utf-8") as f:
    json.dump(apps_data, f, ensure_ascii=False, indent=2)
print(f"\nApps sauvegardees dans googleplay_apps.json")

# ─── ETAPE 4 : Extraire les reviews ────────────────────────────
# On prend les reviews des 5 premieres apps
print("\nExtraction des reviews...")
all_reviews = []

for app_data in apps_data[:5]:
    app_id = app_data["app_id"]
    print(f"  Reviews pour : {app_data['title']}")

    try:
        result, _ = reviews(
            app_id,
            lang="en",
            country="us",
            sort=Sort.MOST_RELEVANT,
            count=20    # 20 reviews par app
        )

        for rev in result:
            all_reviews.append({
                "app_id":    app_id,
                "app_name":  app_data["title"],
                "username":  rev.get("userName", "N/A"),
                "score":     rev.get("score", 0),
                "content":   rev.get("content", "N/A"),
                "date":      str(rev.get("at", "N/A")),
                "thumbs_up": rev.get("thumbsUpCount", 0)
            })

        print(f"    {len(result)} reviews extraites")

    except Exception as e:
        print(f"    Erreur : {e}")

# ─── ETAPE 5 : Sauvegarder les reviews en JSON ─────────────────
with open("googleplay_reviews.json", "w", encoding="utf-8") as f:
    json.dump(all_reviews, f, ensure_ascii=False, indent=2)
print(f"\n{len(all_reviews)} reviews sauvegardees dans googleplay_reviews.json")

# ─── ETAPE 6 : Creer les CSV ───────────────────────────────────
df_apps = pd.DataFrame(apps_data)
df_apps.to_csv("googleplay_apps.csv", index=False, encoding="utf-8")
print("CSV apps : googleplay_apps.csv")

df_reviews = pd.DataFrame(all_reviews)
df_reviews.to_csv("googleplay_reviews.csv", index=False, encoding="utf-8")
print("CSV reviews : googleplay_reviews.csv")

print("\nLab 1 API termine !")