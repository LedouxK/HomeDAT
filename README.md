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
