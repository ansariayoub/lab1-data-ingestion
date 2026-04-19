import requests

# L'URL à scraper
url = "https://github.com/search?q=mental+health+ai&type=repositories"

# Le header fait croire qu'on est un vrai navigateur
# Sans ça, GitHub peut bloquer notre requête (erreur 403)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.8",
}

# Envoyer la requête HTTP à GitHub
response = requests.get(url, headers=headers)

# Afficher le status (200 = OK, 403 = bloqué, 404 = page inexistante)
print(f"Status code : {response.status_code}")

# Sauvegarder le HTML brut dans un fichier texte
if response.status_code == 200:
    with open("github_raw.txt", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("HTML sauvegardé dans github_raw.txt")
else:
    print(f"Erreur : impossible d'accéder à la page ({response.status_code})")