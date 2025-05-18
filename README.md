# Blu-ray Remuxer

Un outil Python pour extraire et remuxer des Blu-rays avec des options de filtrage avancées.

## Fonctionnalités

- Extraction automatique du titre principal d'un Blu-ray
- Détection intelligente du titre le plus long pour les ISOs
- Filtrage des pistes audio et sous-titres
- Support pour les dossiers BDMV et les fichiers ISO
- Interface en ligne de commande interactive

## Prérequis

- Python 3.6+
- MakeMKV
- MKVToolNix

## Installation

1. Clonez ce dépôt :
```bash
git clone [URL_DU_REPO]
cd [NOM_DU_DOSSIER]
```

2. Installez les dépendances Python :
```bash
pip install -r requirements.txt
```

## Utilisation

```bash
python main.py <chemin_source> <dossier_sortie>
```

Exemple :
```bash
python main.py "/chemin/vers/bluray" "output"
```

## Structure du projet

- `main.py` : Point d'entrée principal
- `makemkv_handler.py` : Gestion des opérations MakeMKV
- `mpls_parser.py` : Analyse des fichiers MPLS
- `track_filter.py` : Filtrage des pistes
- `muxer.py` : Gestion du remuxing
- `utils.py` : Fonctions utilitaires
- `language_map.py` : Mapping des langues
- `mediainfo_helper.py` : Aide pour MediaInfo

## Licence

[À DÉFINIR] 