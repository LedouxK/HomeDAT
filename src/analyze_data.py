"""Outils d'analyse du jeu de données DVF."""

import sys
import os
import pyarrow.parquet as pq

def calculer_statistiques(chemin_parquet: str, colonne: str = 'Valeur fonciere', groupe: int = 0) -> dict:
    """Renvoie quelques statistiques simples sur une colonne du parquet."""
    try:
        pq_file = pq.ParquetFile(chemin_parquet)
        table = pq_file.read_row_group(groupe, columns=[colonne])
        arr = table[colonne]
        return {
            'lignes': arr.length(),
            'moyenne': arr.to_pandas().mean()
        }
    except FileNotFoundError:
        print(f"Erreur: Le fichier {chemin_parquet} est introuvable.")
        return {'erreur': 'fichier_introuvable'}
    except Exception as e:
        print(f"Erreur lors de l'analyse des données: {str(e)}")
        return {'erreur': str(e)}

def get_chemin_donnees(relatif_path='data/dvf-2022.parquet'):
    """Obtenir le chemin absolu vers le fichier de données."""
    # Chemin depuis la racine du projet (2 niveaux au-dessus pour src/)
    chemin_projet = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(chemin_projet, relatif_path)

if __name__ == '__main__':
    # Utiliser le chemin fourni en argument ou le chemin par défaut
    chemin_relatif = sys.argv[1] if len(sys.argv) > 1 else 'data/dvf-2022.parquet'
    
    # Convertir en chemin absolu si nécessaire
    if not os.path.isabs(chemin_relatif):
        chemin = get_chemin_donnees(chemin_relatif)
    else:
        chemin = chemin_relatif
        
    print(f"Analyse du fichier: {chemin}")
    stats = calculer_statistiques(chemin)
    
    if 'erreur' not in stats:
        print(f"Nombre de lignes: {stats['lignes']}")
        print(f"Valeur moyenne: {stats['moyenne']:.2f}")
    else:
        print(f"L'analyse a échoué.")
        sys.exit(1)
