import os
import sys
import shutil
from makemkv_handler import get_makemkv_info, parse_title_durations, extract_title
from mpls_parser import find_main_mpls
from track_filter import filter_tracks
from utils import get_source_url, get_playlist_folder
from muxer import build_mkvmerge_command, execute_mux

def main(source_path, output_dir):
    print(f"[DEBUG] Source path: {source_path}")
    source_url = get_source_url(source_path)
    print(f"[DEBUG] Source URL: {source_url}")
    
    makemkv_info = get_makemkv_info(source_url)
    print(f"[DEBUG] MakeMKV info (complet):\n{makemkv_info}")  # Affiche tout
    
    durations = parse_title_durations(makemkv_info)
    print(f"[DEBUG] Durations: {durations}")

    if source_url.startswith("file://"):
        playlist_folder = get_playlist_folder(source_path)
        print(f"[DEBUG] Playlist folder: {playlist_folder}")
        mpls_file, mpls_duration = find_main_mpls(playlist_folder)
        print(f"[DEBUG] MPLS file: {mpls_file}, duration: {mpls_duration}")
        title_id = min(durations, key=lambda t: abs(durations[t] - mpls_duration))
        print(f"[+] Playlist détectée : {os.path.basename(mpls_file)} ({mpls_duration/60:.2f} min)")
    else:
        title_id = max(durations, key=durations.get)
        print(f"[+] ISO : titre le plus long détecté ({durations[title_id]/60:.2f} min)")

    # Nettoyage du dossier de sortie
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    extract_title(source_url, title_id, output_dir)

    mkv_files = [f for f in os.listdir(output_dir) if f.endswith(".mkv")]
    if not mkv_files:
        print("[!] Aucun fichier MKV trouvé.")
        return

    input_mkv = os.path.join(output_dir, mkv_files[0])
    output_mkv = os.path.join(output_dir, "filtered_remux.mkv")

    print("\n=== Lancement du muxing optimisé ===")
    print("Entrez le titre de la vidéo (ex: Captain America) :")
    video_title = input("> ").strip()

    print("Entrez le tag de la VF (VFF, VFQ, VFi, VOF...) :")
    vf_tag = input("> ").strip().upper()

    # Construction et exécution de la commande mkvmerge
    cmd = build_mkvmerge_command(input_mkv, output_mkv)
    if execute_mux(cmd):
        print(f"[✓] Remux final : {output_mkv}")
    else:
        print("[!] Le muxing a échoué.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage : python main.py <source ISO ou BDMV> <dossier de sortie>")
        sys.exit(1)

    source = os.path.abspath(sys.argv[1])
    output = os.path.abspath(sys.argv[2])
    main(source, output)
