import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re

url = "https://github.com/search?q=mental+health+ai&type=repositories"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.8",
}

response = requests.get(url, headers=headers)
print(f"Status : {response.status_code}")

# Parser le HTML
soup = BeautifulSoup(response.text, "html.parser")

# Les données sont dans un script JSON embarqué dans la page
# On cherche le script qui contient les résultats
script_tag = soup.find("script", attrs={"data-target": "react-app.embeddedData"})

if not script_tag:
    print("Script JSON non trouvé, essai méthode 2...")
    # Méthode 2 : chercher dans tous les scripts
    for script in soup.find_all("script"):
        if script.string and "mental-health" in str(script.string):
            script_tag = script
            break

if script_tag and script_tag.string:
    print("Données JSON trouvées !")
    
    # Parser le JSON
    json_data = json.loads(script_tag.string)
    
    # Naviguer dans le JSON pour trouver les repos
    # La structure : payload > results
    try:
        results = json_data["payload"]["results"]
        print(f"{len(results)} repos trouvés !")
        
        data = []
        for repo in results:
            title = repo.get("hl_name", "N/A")
            # Nettoyer les balises <em> du titre
            title = re.sub(r'<[^>]+>', '', title)
            
            description = repo.get("hl_trunc_description", "N/A")
            description = re.sub(r'<[^>]+>', '', str(description))
            
            stars = repo.get("followers", "N/A")
            language = repo.get("color", "N/A")
            language = repo.get("language", "N/A") if "language" in repo else "N/A"
            updated = repo.get("repo", {}).get("repository", {}).get("updated_at", "N/A")
            repo_name = repo.get("repo", {}).get("repository", {}).get("name", "N/A")
            owner = repo.get("repo", {}).get("repository", {}).get("owner_login", "N/A")
            link = f"https://github.com/{owner}/{repo_name}"
            
            data.append({
                "title": title,
                "url": link,
                "description": description,
                "stars": stars,
                "language": language,
                "last_updated": updated
            })
        
        # Créer DataFrame et sauvegarder
        df = pd.DataFrame(data)
        print(df)
        print(f"\nTotal : {len(df)} repos extraits")
        df.to_csv("github_repos_page1.csv", index=False, encoding="utf-8")
        print("Sauvegardé dans github_repos_page1.csv")
        
    except KeyError as e:
        print(f"Clé JSON non trouvée : {e}")
        print("Structure JSON reçue :", list(json_data.keys()))
else:
    print("Aucune donnée JSON trouvée")