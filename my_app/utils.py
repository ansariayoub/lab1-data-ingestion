# utils.py - Fonctions de recuperation de donnees

from google_play_scraper import search, reviews, Sort
import pandas as pd
import json
import os

def search_apps(query, n_hits=20):
    """
    Recherche des apps sur Google Play et retourne un DataFrame
    Parametres :
        query   : terme de recherche (ex: "mental health ai")
        n_hits  : nombre de resultats voulus
    Retourne :
        DataFrame avec les colonnes : app_id, title, developer,
        score, ratings, installs, free, genre, description
    """
    try:
        resultats = search(
            query,
            lang="en",
            country="us",
            n_hits=n_hits
        )

        apps = []
        for r in resultats:
            apps.append({
                "app_id":      r.get("appId", "N/A"),
                "title":       r.get("title", "N/A"),
                "developer":   r.get("developer", "N/A"),
                "score":       r.get("score", 0),
                "ratings":     r.get("ratings", 0),
                "installs":    r.get("installs", "N/A"),
                "free":        "Free" if r.get("free", True) else "Paid",
                "price":       r.get("price", 0),
                "genre":       r.get("genre", "N/A"),
                "description": r.get("description", "N/A")[:300],
                "url":         r.get("url", "N/A")
            })

        return pd.DataFrame(apps)

    except Exception as e:
        print(f"Erreur search_apps : {e}")
        return pd.DataFrame()


def get_reviews(app_id, app_name, count=10):
    """
    Recupere les reviews d'une app
    Retourne une liste de dictionnaires
    """
    try:
        result, _ = reviews(
            app_id,
            lang="en",
            country="us",
            sort=Sort.MOST_RELEVANT,
            count=count
        )

        revs = []
        for rev in result:
            revs.append({
                "app_id":    app_id,
                "app_name":  app_name,
                "username":  rev.get("userName", "N/A"),
                "score":     rev.get("score", 0),
                "content":   rev.get("content", "N/A"),
                "date":      str(rev.get("at", "N/A")),
                "thumbs_up": rev.get("thumbsUpCount", 0)
            })

        return revs

    except Exception as e:
        print(f"Erreur get_reviews : {e}")
        return []