# 1_Results_Table.py - Page des résultats de recherche

import streamlit as st
import sys
import os

# Ajouter le dossier parent au path pour importer utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import search_apps

# ─── Configuration ────────────────────────────────────────────
st.set_page_config(page_title="Results Table", page_icon="📋", layout="wide")

st.title("📋 Résultats de Recherche")
st.markdown("---")

# ─── Barre de recherche ───────────────────────────────────────
st.header("🔍 Rechercher des applications")

col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_input(
        "Terme de recherche",
        value="mental health ai",
        placeholder="Ex: mental health ai, wellness app..."
    )

with col2:
    n_hits = st.number_input("Nombre de résultats", min_value=5, max_value=50, value=20)

# ─── Bouton de recherche ──────────────────────────────────────
if st.button("🔍 Rechercher", type="primary"):

    # Spinner pendant la recherche
    with st.spinner(f"Recherche de '{query}' sur Google Play..."):
        df = search_apps(query, n_hits=n_hits)

    if df.empty:
        st.error("Aucun résultat trouvé. Essaie un autre terme.")
    else:
        # Sauvegarder dans la session pour la page 2
        st.session_state["search_results"] = df
        st.session_state["search_query"] = query
        st.success(f"✅ {len(df)} applications trouvées !")

# ─── Afficher les resultats ───────────────────────────────────
if "search_results" in st.session_state:
    df = st.session_state["search_results"]

    # Métriques en haut
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📱 Apps trouvées", len(df))
    col2.metric("⭐ Score moyen", f"{df['score'].mean():.2f}")
    col3.metric("🆓 Apps gratuites", len(df[df["free"] == "Free"]))
    col4.metric("💰 Apps payantes", len(df[df["free"] == "Paid"]))

    st.markdown("---")

    # Filtres
    st.subheader("🔧 Filtres")
    col1, col2 = st.columns(2)

    with col1:
        genres = ["Tous"] + sorted(df["genre"].unique().tolist())
        genre_filtre = st.selectbox("Genre", genres)

    with col2:
        score_min = st.slider("Score minimum", 0.0, 5.0, 0.0, 0.1)

    # Appliquer les filtres
    df_filtre = df.copy()
    if genre_filtre != "Tous":
        df_filtre = df_filtre[df_filtre["genre"] == genre_filtre]
    df_filtre = df_filtre[df_filtre["score"] >= score_min]

    # Tableau des résultats
    st.subheader(f"📊 {len(df_filtre)} résultats")
    st.dataframe(
        df_filtre[[
            "title", "developer", "score",
            "ratings", "installs", "free", "genre"
        ]],
        use_container_width=True,
        column_config={
            "title":     st.column_config.TextColumn("Nom"),
            "developer": st.column_config.TextColumn("Développeur"),
            "score":     st.column_config.NumberColumn("Score ⭐", format="%.2f"),
            "ratings":   st.column_config.NumberColumn("Nb Ratings"),
            "installs":  st.column_config.TextColumn("Installations"),
            "free":      st.column_config.TextColumn("Gratuit/Payant"),
            "genre":     st.column_config.TextColumn("Genre"),
        }
    )

    # Bouton de téléchargement
    csv = df_filtre.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Télécharger CSV",
        csv,
        "resultats.csv",
        "text/csv"
    )
else:
    st.info("👆 Entre un terme de recherche et clique sur Rechercher !")