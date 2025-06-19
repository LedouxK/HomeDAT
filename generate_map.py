"""Fonctions pour générer une carte Folium."""

import folium
import pandas as pd


def generate_price_map(df: pd.DataFrame) -> folium.Map:
    """Génère une carte avec des cercles proportionnels aux prix."""
    m = folium.Map(location=[45.75, 4.85], zoom_start=12)
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=5,
            fill=True,
            color="blue",
            fill_color="blue",
            popup=f"{row['quartier']} - {row['prix_m2']} €/m²",
        ).add_to(m)
    return m
