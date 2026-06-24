# 2_Visualizations.py - Page des visualisations

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Visualizations", page_icon="📈", layout="wide")
st.title("📈 Visualisations — Analyse Concurrentielle")
st.markdown("---")

# ─── Verifier que les données existent ───────────────────────
if "search_results" not in st.session_state:
    st.warning("⚠️ Pas de données ! Va sur la page Results Table et lance une recherche.")
    st.stop()

df = st.session_state["search_results"]
query = st.session_state.get("search_query", "")

st.subheader(f"Analyse pour : **{query}** — {len(df)} applications")
st.markdown("---")

# ─── SIDEBAR : Filtres ────────────────────────────────────────
st.sidebar.header("🔧 Filtres")
app_ids = ["Tous"] + df["app_id"].tolist()
app_filtre = st.sidebar.selectbox("Filtrer par App ID", app_ids)

genres_dispo = ["Tous"] + sorted(df["genre"].unique().tolist())
genre_filtre = st.sidebar.selectbox("Genre", genres_dispo)

score_min = st.sidebar.slider("Score minimum", 0.0, 5.0, 0.0)

# Appliquer les filtres
df_viz = df.copy()
if app_filtre != "Tous":
    df_viz = df_viz[df_viz["app_id"] == app_filtre]
if genre_filtre != "Tous":
    df_viz = df_viz[df_viz["genre"] == genre_filtre]
df_viz = df_viz[df_viz["score"] >= score_min]

st.sidebar.metric("Apps affichées", len(df_viz))

# ─── LIGNE 1 : Métriques ─────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("📱 Apps", len(df_viz))
col2.metric("⭐ Score moyen", f"{df_viz['score'].mean():.2f}" if len(df_viz) > 0 else "N/A")
col3.metric("🆓 Gratuites", len(df_viz[df_viz["free"] == "Free"]))
col4.metric("💰 Payantes", len(df_viz[df_viz["free"] == "Paid"]))

st.markdown("---")

# ─── LIGNE 2 : Top Apps + Distribution Scores ────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 10 Apps par Score")
    top10 = df_viz.nlargest(10, "score")
    fig1 = px.bar(
        top10,
        x="score",
        y="title",
        orientation="h",
        color="score",
        color_continuous_scale="Blues",
        labels={"score": "Score", "title": "Application"}
    )
    fig1.update_layout(yaxis={"categoryorder": "total ascending"}, height=400)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📊 Distribution des Scores")
    fig2 = px.histogram(
        df_viz,
        x="score",
        nbins=10,
        color_discrete_sequence=["#2E75B6"],
        labels={"score": "Score", "count": "Nombre d'apps"}
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ─── LIGNE 3 : Pie Chart + Top par Ratings ───────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("🆓 Apps Gratuites vs Payantes")
    free_counts = df_viz["free"].value_counts().reset_index()
    free_counts.columns = ["type", "count"]
    fig3 = px.pie(
        free_counts,
        values="count",
        names="type",
        color_discrete_sequence=["#1D9E75", "#2E75B6"]
    )
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("📈 Top 10 Apps par Nombre de Ratings")
    top_ratings = df_viz.nlargest(10, "ratings")
    fig4 = px.bar(
        top_ratings,
        x="title",
        y="ratings",
        color="score",
        color_continuous_scale="Viridis",
        labels={"ratings": "Nombre de Ratings", "title": "Application"}
    )
    fig4.update_layout(xaxis_tickangle=-45, height=400)
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ─── LIGNE 4 : Distribution des Genres ──────────────────────
st.subheader("🎯 Distribution par Genre")
genre_counts = df_viz["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]
fig5 = px.bar(
    genre_counts,
    x="genre",
    y="count",
    color="count",
    color_continuous_scale="Blues",
    labels={"genre": "Genre", "count": "Nombre d'apps"}
)
st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# ─── LIGNE 5 : WordCloud ─────────────────────────────────────
st.subheader("☁️ WordCloud des Descriptions")
try:
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    texte = " ".join(df_viz["description"].dropna().tolist())
    if texte.strip():
        wc = WordCloud(
            width=800, height=400,
            background_color="white",
            colormap="Blues",
            max_words=100
        ).generate(texte)

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.info("Pas assez de descriptions pour le WordCloud")

except ImportError:
    st.warning("Installe wordcloud : pip install wordcloud")

st.markdown("---")
st.caption("Lab 2 — Data Applications with Streamlit | ENSIAS 2026")