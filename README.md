# HomeDAT

Exemple de projet pour explorer les données du marché immobilier français.

## Installation

```bash
pip install -r requirements.txt
```

## Télécharger le jeu de données

```bash
python src/download_data.py
```

## Analyse basique

```bash
python src/analyze_data.py data/dvf-2022.parquet
```

## Application Streamlit

Lancer l'application interactive :

```bash
streamlit run app/streamlit_app.py
```

## HomePedia PoC

Ce prototype propose une exploration rapide du marché immobilier à Lyon.

### Lancer l'application principale

```bash
streamlit run main.py
```

### Détails des fichiers

- `main.py` : application Streamlit qui affiche une carte, les données et l'analyse de sentiment.
- `generate_map.py` : fonctions pour créer la carte Folium.
- `sentiment_analysis.py` : charge les commentaires, calcule un score moyen et génère un wordcloud.
- `spark/process_prices.py` : exemple de script Spark pour résumer les prix.
- `data/lyon_prices.csv` : données factices de prix au m².
- `data/lyon_comments.json` : quelques commentaires factices.
