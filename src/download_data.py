"""Script pour télécharger le jeu de données DVF."""

import os
import requests

def telecharger_jeu_donnees(url_dataset: str, chemin_dest: str) -> str:
    """Télécharge un fichier depuis l'URL donnée."""
    os.makedirs(os.path.dirname(chemin_dest), exist_ok=True)
    with requests.get(url_dataset, stream=True) as r:
        r.raise_for_status()
        with open(chemin_dest, 'wb') as f:
            for morceau in r.iter_content(chunk_size=8192):
                if morceau:
                    f.write(morceau)
    return chemin_dest

if __name__ == '__main__':
    url = 'https://static.data.gouv.fr/resources/dvf-2022-format-parquet/20231108-151100/dvf-2022.parquet'
    dest = os.path.join('data', 'dvf-2022.parquet')
    print(f'Téléchargement de {url}…')
    telecharger_jeu_donnees(url, dest)
    print(f'Fichier enregistré dans {dest}')
