import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.8",
}

# Le lab dit "refrain from doing it dynamically"
# = on liste les pages manuellement
urls = [
    "https://github.com/search?q=mental+health+ai&type=repositories&p=1",
    "https://github.com/search?q=mental+health+ai&type=repositories&p=2",
    "https://github.com/search?q=mental+health+ai&type=repositories&p=3",
    "https://github.com/search?q=mental+health+ai&type=repositories&p=4",
    "https://github.com/search?q=mental+health+ai&type=repositories&p=5",
]

all_data = []

for page_url in urls:
    print(f"\nScraping : {page_url}")
    
    response = requests.get(page_url, headers=headers)
    print(f"Status : {response.status_code}")
    
    if response.status_code != 200:
        print("Erreur sur cette page, on passe à la suivante")
        continue
    
    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("script", attrs={"data-target": "react-app.embeddedData"})
    
    if not script_tag or not script_tag.string:
        print("Pas de données JSON sur cette page")
        continue
    
    json_data = json.loads(script_tag.string)
    
    try:
        results = json_data["payload"]["results"]
        print(f"{len(results)} repos trouvés sur cette page")
        
        for repo in results:
            title = re.sub(r'<[^>]+>', '', repo.get("hl_name", "N/A"))
            description = re.sub(r'<[^>]+>', '', str(repo.get("hl_trunc_description", "N/A")))
            stars = repo.get("followers", "N/A")
            language = repo.get("language", "N/A")
            updated = repo.get("repo", {}).get("repository", {}).get("updated_at", "N/A")
            repo_name = repo.get("repo", {}).get("repository", {}).get("name", "N/A")
            owner = repo.get("repo", {}).get("repository", {}).get("owner_login", "N/A")
            link = f"https://github.com/{owner}/{repo_name}"
            
            all_data.append({
                "title": title,
                "url": link,
                "description": description,
                "stars": stars,
                "language": language,
                "last_updated": updated
            })
    
    except KeyError as e:
        print(f"Clé JSON non trouvée : {e}")
    
    # Attendre 2 secondes entre chaque page (respecter le serveur)
    print("Attente 2 secondes...")
    time.sleep(2)

# Supprimer les doublons et sauvegarder
df = pd.DataFrame(all_data)
df = df.drop_duplicates(subset="title")
print(f"\nTotal final : {len(df)} repos extraits")
print(df[["title", "stars", "language"]])
df.to_csv("github_repos_all.csv", index=False, encoding="utf-8")
print("\nSauvegardé dans github_repos_all.csv")