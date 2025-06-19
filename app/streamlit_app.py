import streamlit as st
import pandas as pd
import os
import sys
import json
import matplotlib.pyplot as plt
from streamlit_folium import st_folium

# Ajouter le dossier principal et src/ au path pour les imports
proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(proj_path, 'src')
sys.path.append(src_path)
sys.path.append(proj_path)

# Importer les utilitaires communs
from utils import get_chemin_donnees, charger_donnees_parquet
from generate_map import generate_price_map
from sentiment_analysis import analyze_comments

# Définir les chemins des fichiers
CHEMIN_DVF = get_chemin_donnees('data/dvf-2022.parquet')
PRICES_PATH = os.path.join(proj_path, "data/lyon_prices.csv")
COMMENTS_PATH = os.path.join(proj_path, "data/lyon_comments.json")


def load_prices():
    """Charge les données de prix de Lyon."""
    try:
        return pd.read_csv(PRICES_PATH)
    except Exception as e:
        st.error(f"Erreur lors du chargement des prix: {str(e)}")
        return pd.DataFrame()


st.title('Explorateur Immobilier HomeDAT')

# Créer un menu latéral pour naviguer entre les sections
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choisissez une section",
    ["Carte des prix à Lyon", "Analyse des sentiments", "Données DVF"]
)

# Section 1: Carte des prix à Lyon
if page == "Carte des prix à Lyon":
    st.header("Marché immobilier à Lyon")
    
    df = load_prices()
    
    if not df.empty:
        # Filtres
        st.sidebar.header("Filtres")
        quartiers = st.sidebar.multiselect(
            "Quartiers", options=df["quartier"].unique().tolist(), 
            default=list(df["quartier"].unique())
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
    else:
        st.warning("Données de prix indisponibles pour Lyon")

# Section 2: Analyse des sentiments
elif page == "Analyse des sentiments":
    st.header("Analyse de sentiment des commentaires")
    
    try:
        score, wc = analyze_comments(COMMENTS_PATH)
        st.write("Score moyen de sentiment:", round(score, 2), 
                 "(de -1: très négatif à +1: très positif)")
        
        # Affichage du nuage de mots
        fig, ax = plt.subplots()
        ax.imshow(wc)
        ax.axis("off")
        st.pyplot(fig)
        
        # Charger les commentaires pour affichage
        try:
            with open(COMMENTS_PATH, "r", encoding="utf-8") as f:
                comments = json.load(f)
                
            st.subheader("Exemples de commentaires")
            for i, item in enumerate(comments[:5]):  # Limite à 5 commentaires
                st.text_area(f"Commentaire {i+1}", item["comment"], height=100)
        except Exception as e:
            st.error(f"Erreur lors du chargement des commentaires: {str(e)}")
            
    except Exception as e:
        st.error(f"Erreur lors de l'analyse des sentiments: {str(e)}")

# Section 3: Données DVF
elif page == "Données DVF":
    st.header("Données DVF 2022")
    st.write(f"Chemin d'accès au fichier de données : {CHEMIN_DVF}")

    # Utiliser une gestion d'erreurs robuste pour le chargement des données
    try:
        df = charger_donnees_parquet(CHEMIN_DVF, colonnes=['Commune', 'Valeur fonciere'])
        
        # Interface avec les données
        st.write('Extrait de lignes :')
        st.dataframe(df.head())
        
        st.write('Valeur foncière moyenne (échantillon) :', df['Valeur fonciere'].mean())
        
        # Quelques visualisations supplémentaires
        st.subheader('Distribution des valeurs foncières')
        st.bar_chart(df['Valeur fonciere'].value_counts())
        
    except FileNotFoundError:
        st.error(f"Le fichier de données DVF est introuvable : {CHEMIN_DVF}")
        st.info("Exécutez 'python src/download_data.py' pour télécharger les données.")
    except Exception as e:
        st.error(f"Erreur lors du chargement des données DVF : {str(e)}")

