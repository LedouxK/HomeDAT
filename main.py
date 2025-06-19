"""Application Streamlit HomePedia."""

import json
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

from generate_map import generate_price_map
from sentiment_analysis import analyze_comments


PRICES_PATH = "data/lyon_prices.csv"
COMMENTS_PATH = "data/lyon_comments.json"


def load_prices():
    return pd.read_csv(PRICES_PATH)


def main():
    st.title("HomePedia - Marché immobilier à Lyon")

    df = load_prices()

    st.sidebar.header("Filtres")
    quartiers = st.sidebar.multiselect(
        "Quartiers", options=df["quartier"].unique().tolist(), default=list(df["quartier"].unique())
    )
    min_p, max_p = int(df.prix_m2.min()), int(df.prix_m2.max())
    price_min, price_max = st.sidebar.slider(
        "Prix au m²", min_p, max_p, (min_p, max_p)
    )

    filtered = df[df["quartier"].isin(quartiers)]
    filtered = filtered[(filtered.prix_m2 >= price_min) & (filtered.prix_m2 <= price_max)]

    st.subheader("Carte des prix")
    fmap = generate_price_map(filtered)
    st_folium(fmap, width=700, height=500)

    st.subheader("Données")
    st.dataframe(filtered)

    st.subheader("Analyse de sentiment des commentaires")
    score, wc = analyze_comments(COMMENTS_PATH)
    st.write("Score moyen :", round(score, 2))
    fig, ax = plt.subplots()
    ax.imshow(wc)
    ax.axis("off")
    st.pyplot(fig)


if __name__ == "__main__":
    main()
