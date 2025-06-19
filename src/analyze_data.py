"""Outils d'analyse du jeu de données DVF."""

import sys
import pyarrow.parquet as pq

def calculer_statistiques(chemin_parquet: str, colonne: str = 'Valeur fonciere', groupe: int = 0) -> dict:
    """Renvoie quelques statistiques simples sur une colonne du parquet."""
    pq_file = pq.ParquetFile(chemin_parquet)
    table = pq_file.read_row_group(groupe, columns=[colonne])
    arr = table[colonne]
    return {
        'lignes': arr.length(),
        'moyenne': arr.to_pandas().mean()
    }

if __name__ == '__main__':
    chemin = sys.argv[1] if len(sys.argv) > 1 else 'data/dvf-2022.parquet'
    stats = calculer_statistiques(chemin)
    print(stats)
