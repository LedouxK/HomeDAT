import streamlit as st
import pyarrow.parquet as pq
import pandas as pd
import os

def charger_echantillon(chemin: str, colonnes=None, groupe=0):
    """Charge un sous-ensemble du fichier parquet."""
    pq_file = pq.ParquetFile(chemin)
    table = pq_file.read_row_group(groupe, columns=colonnes)
    return table.to_pandas()

st.title('Explorateur Immobilier HomeDAT')

# Chemin absolu pour accéder au fichier de données
CHEMIN_DONNEES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dvf-2022.parquet')
st.write(f"Chemin d'accès au fichier de données : {CHEMIN_DONNEES}")

df = charger_echantillon(CHEMIN_DONNEES, colonnes=['Commune', 'Valeur fonciere'])

st.write('Extrait de lignes :')
st.dataframe(df.head())

st.write('Valeur foncière moyenne (échantillon) :', df['Valeur fonciere'].mean())
