"""Script pour télécharger le jeu de données DVF."""

import os
import sys
import requests
import time

# Importer les utilitaires communs
from utils import get_chemin_donnees

def telecharger_jeu_donnees(url_dataset: str, chemin_dest: str) -> str:
    """Télécharge un fichier depuis l'URL donnée avec barre de progression."""
    try:
        # Créer le dossier parent s'il n'existe pas
        os.makedirs(os.path.dirname(chemin_dest), exist_ok=True)
        
        with requests.get(url_dataset, stream=True) as r:
            r.raise_for_status()
            taille_totale = int(r.headers.get('content-length', 0))
            taille_telecharge = 0
            derniere_maj = time.time()
            with open(chemin_dest, 'wb') as f:
                for morceau in r.iter_content(chunk_size=8192):
                    if morceau:
                        f.write(morceau)
                        taille_telecharge += len(morceau)
                        
                        # Afficher la progression toutes les 0.5 secondes
                        maintenant = time.time()
                        if maintenant - derniere_maj > 0.5:
                            pourcentage = 100 * taille_telecharge / taille_totale if taille_totale > 0 else 0
                            print(f"Téléchargement: {taille_telecharge / 1_000_000:.1f} Mo / "
                                  f"{taille_totale / 1_000_000:.1f} Mo ({pourcentage:.1f}%)")
                            derniere_maj = maintenant
        return chemin_dest
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement: {str(e)}")
        return None

if __name__ == '__main__':
    url = 'https://static.data.gouv.fr/resources/dvf-2022-format-parquet/20231108-151100/dvf-2022.parquet'
    
    # Utiliser le chemin absolu pour le fichier de destination
    dest_relatif = 'data/dvf-2022.parquet'
    dest_absolu = get_chemin_donnees(dest_relatif)
    
    print(f'Téléchargement de {url}')
    print(f'Destination: {dest_absolu}')
    
    # Télécharger le fichier avec gestion d'erreurs
    resultat = telecharger_jeu_donnees(url, dest_absolu)
    
    if resultat:
        print(f'\nFichier téléchargé avec succès dans {dest_absolu}')
        print(f'Taille du fichier: {os.path.getsize(dest_absolu) / 1_000_000:.1f} Mo')
    else:
        print('\nLe téléchargement a échoué.')
        sys.exit(1)
