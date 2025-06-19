"""Utilitaires communs pour le projet HomeDAT."""

import os
import pyarrow.parquet as pq
import pandas as pd


def get_chemin_donnees(relatif_path='data/dvf-2022.parquet'):
    """
    Obtenir le chemin absolu vers un fichier dans le projet.
    
    Args:
        relatif_path (str): Chemin relatif depuis la racine du projet
        
    Returns:
        str: Chemin absolu vers le fichier
    """
    # Déterminer la racine du projet (2 niveaux au-dessus du dossier src/)
    chemin_projet = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(chemin_projet, relatif_path)


def charger_donnees_parquet(chemin_parquet, colonnes=None, groupe=0):
    """
    Charge un sous-ensemble du fichier parquet dans un DataFrame pandas.
    
    Args:
        chemin_parquet (str): Chemin vers le fichier parquet
        colonnes (list): Liste des colonnes à charger (None pour toutes)
        groupe (int): Index du groupe de lignes à charger
        
    Returns:
        pd.DataFrame: DataFrame contenant les données demandées
        
    Raises:
        FileNotFoundError: Si le fichier n'est pas trouvé
        Exception: Autres erreurs survenues lors du chargement
    """
    try:
        pq_file = pq.ParquetFile(chemin_parquet)
        table = pq_file.read_row_group(groupe, columns=colonnes)
        return table.to_pandas()
    except FileNotFoundError:
        raise FileNotFoundError(f"Le fichier {chemin_parquet} est introuvable.")
    except Exception as e:
        raise Exception(f"Erreur lors du chargement des données: {str(e)}")
