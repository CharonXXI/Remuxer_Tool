import os
import sys
import subprocess
from track_helper import (
    select_video_track,
    select_audio_tracks,
    select_subtitle_tracks
)

def check_dependencies():
    """Vérifie que les dépendances nécessaires sont installées."""
    required_tools = ["mkvmerge", "mediainfo"]
    missing_tools = []
    
    for tool in required_tools:
        try:
            subprocess.run([tool, "--version"], capture_output=True, check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"[ERREUR] Outils manquants : {', '.join(missing_tools)}")
        print("Veuillez les installer avant de continuer.")
        sys.exit(1)

def get_input_file():
    """Demande et vérifie le fichier d'entrée."""
    while True:
        input_file = input("\nChemin du fichier MKV source : ").strip()
        if not input_file:
            print("[ERREUR] Chemin vide.")
            continue
        if not os.path.isfile(input_file):
            print(f"[ERREUR] Fichier introuvable : {input_file}")
            continue
        if not input_file.lower().endswith('.mkv'):
            print("[ERREUR] Le fichier doit être au format MKV.")
            continue
        return input_file

def get_output_file():
    """Demande et vérifie le fichier de sortie."""
    while True:
        output_file = input("Chemin du fichier MKV de sortie : ").strip()
        if not output_file:
            print("[ERREUR] Chemin vide.")
            continue
        if not output_file.lower().endswith('.mkv'):
            print("[ERREUR] Le fichier de sortie doit être au format MKV.")
            continue
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except OSError:
                print(f"[ERREUR] Impossible de créer le dossier : {output_dir}")
                continue
        return output_file

def build_mkvmerge_command(input_file, output_file):
    """Construit la commande mkvmerge avec les paramètres utilisateur."""
    print("\n=== Configuration du muxing ===")
    
    # Demande du titre
    while True:
        video_title = input("\nTitre de la vidéo (ex: Captain America) : ").strip()
        if video_title:
            break
        print("[ERREUR] Le titre ne peut pas être vide.")

    # Demande du tag VF
    while True:
        vf_tag = input("Tag de la VF (VFF, VFQ, VFi, VOF...) : ").strip().upper()
        if vf_tag:
            break
        print("[ERREUR] Le tag VF ne peut pas être vide.")

    print("\nAnalyse des pistes...")
    try:
        video_track = select_video_track(input_file)
        vo_audio, vf_audio = select_audio_tracks(input_file)
        subtitle_tracks = select_subtitle_tracks(input_file)
    except Exception as e:
        print(f"[ERREUR] Impossible d'analyser les pistes : {str(e)}")
        sys.exit(1)

    cmd = ["mkvmerge", "-o", output_file]

    # Vidéo
    video_id = video_track["@typeorder"]
    cmd += [
        "--track-name", f"{video_id}:{video_title}",
        "--language", f"{video_id}:und",
        "--default-track", f"{video_id}:yes",
        input_file
    ]

    # Audio VO
    if vo_audio:
        a = vo_audio["info"]
        track_id = vo_audio["@typeorder"]
        name = f'{a["language_name"]} {a["codec"]} {a["channels"]} @ {a["bitrate"]}'
        cmd += [
            "--track-name", f"{track_id}:{name}",
            "--language", f"{track_id}:{a['language_code']}",
            "--default-track", f"{track_id}:yes"
        ]

    # Audio VF
    if vf_audio:
        a = vf_audio["info"]
        track_id = vf_audio["@typeorder"]
        name = f'{vf_tag} {a["codec"]} {a["channels"]} @ {a["bitrate"]}'
        cmd += [
            "--track-name", f"{track_id}:{name}",
            "--language", f"{track_id}:{a['language_code']}",
            "--default-track", f"{track_id}:no"
        ]

    # Sous-titres FR
    for sub in subtitle_tracks:
        s = sub["info"]
        track_id = sub["@typeorder"]
        cmd += [
            "--track-name", f"{track_id}:{s['title']}",
            "--language", f"{track_id}:{s['language_code']}",
            "--default-track", f"{track_id}:no"
        ]

    cmd.append(input_file)
    return cmd

def execute_mux(cmd):
    """Exécute la commande mkvmerge."""
    print("\n=== Commande mkvmerge ===")
    print(" ".join(cmd))
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("\n[✓] Muxing terminé avec succès !")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[ERREUR] Échec du muxing : {e.stderr}")
        return False

def main():
    """Point d'entrée principal du script."""
    print("=== MKV Muxer ===")
    print("Ce script permet de créer un fichier MKV optimisé avec les meilleures pistes.")
    
    # Vérification des dépendances
    check_dependencies()
    
    # Récupération des fichiers
    input_file = get_input_file()
    output_file = get_output_file()
    
    # Construction et exécution de la commande
    cmd = build_mkvmerge_command(input_file, output_file)
    if execute_mux(cmd):
        print(f"\nFichier final créé : {output_file}")
    else:
        print("\n[ERREUR] Le muxing a échoué.")
        sys.exit(1)

if __name__ == "__main__":
    main()
