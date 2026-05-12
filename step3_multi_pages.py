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

all_data = []
page = 1
total_pages = None

while True:
    url = f"https://github.com/search?q=mental+health+ai&type=repositories&p={page}"
    print(f"Scraping page {page}...")

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Erreur status {response.status_code}, on arrete")
        break

    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("script", attrs={"data-target": "react-app.embeddedData"})

    if not script_tag or not script_tag.string:
        print("Plus de donnees, on arrete")
        break

    json_data = json.loads(script_tag.string)
    payload = json_data["payload"]
    results = payload.get("results", [])

    # Detecter automatiquement le nombre total de pages
    if total_pages is None:
        total_pages = payload.get("page_count", 1)
        print(f"Nombre total de pages detecte : {total_pages}")

    if not results:
        print("Plus de resultats, on arrete")
        break

    print(f"{len(results)} repos trouves sur la page {page}")

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

    if total_pages and page >= total_pages:
        print(f"Derniere page atteinte ({total_pages}), on arrete")
        break

    page += 1
    print("Attente 2 secondes...")
    time.sleep(2)

df = pd.DataFrame(all_data)
df = df.drop_duplicates(subset="title")
print(f"\nTotal : {len(df)} repos extraits sur {page} pages")
df.to_csv("github_repos_dynamic.csv", index=False, encoding="utf-8")
print("Sauvegarde dans github_repos_dynamic.csv")