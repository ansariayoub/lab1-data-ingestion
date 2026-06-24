# Home.py - Page d'accueil de l'application

import streamlit as st

# ─── Configuration de la page ──────────────────────────────────
st.set_page_config(
    page_title="Competitor Analysis App",
    page_icon="📊",
    layout="wide"
)

# ─── Titre et description ──────────────────────────────────────
st.title("📊 Mental Health Apps — Competitor Analysis")
st.markdown("---")

# ─── Description du projet ────────────────────────────────────
st.header("📌 A propos de cette application")
st.write("""
Cette application analyse les applications concurrentes dans le domaine
de la **santé mentale et du bien-être** en utilisant les données du
Google Play Store.
""")

# ─── Fonctionnalites ──────────────────────────────────────────
st.header("🚀 Fonctionnalités")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    **📋 Page 1 — Résultats**
    - Recherche d'apps par mot-clé
    - Tableau interactif des résultats
    - Filtres et tri des données
    """)

with col2:
    st.success("""
    **📈 Page 2 — Visualisations**
    - Distribution des ratings
    - Top apps par popularité
    - Apps gratuites vs payantes
    - WordCloud des descriptions
    """)

# ─── Comment utiliser ─────────────────────────────────────────
st.header("📖 Comment utiliser")
st.write("""
1. Va sur la page **Results Table** dans le menu à gauche
2. Entre un terme de recherche (ex: "mental health ai")
3. Clique sur **Rechercher**
4. Va sur la page **Visualizations** pour voir les graphiques
""")

# ─── Informations ─────────────────────────────────────────────
st.header("ℹ️ Informations")
st.write("""
- **Source de données** : Google Play Store via google-play-scraper
- **Développé par** : Ayoub Ansari
- **Lab** : Introduction to Data Applications — ENSIAS 2026
""")

st.markdown("---")
st.caption("Lab 2 — Data Applications with Streamlit | ENSIAS 2026")