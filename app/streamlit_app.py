import streamlit as st
import pyarrow.parquet as pq
import pandas as pd

def charger_echantillon(chemin: str, colonnes=None, groupe=0):
    """Charge un sous-ensemble du fichier parquet."""
    pq_file = pq.ParquetFile(chemin)
    table = pq_file.read_row_group(groupe, columns=colonnes)
    return table.to_pandas()

st.title('Explorateur Immobilier HomeDAT')

CHEMIN_DONNEES = 'data/dvf-2022.parquet'

df = charger_echantillon(CHEMIN_DONNEES, colonnes=['Commune', 'Valeur fonciere'])

st.write('Extrait de lignes :')
st.dataframe(df.head())

st.write('Valeur foncière moyenne (échantillon) :', df['Valeur fonciere'].mean())
