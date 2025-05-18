import subprocess
import json
import os
import sys

def get_track_info(mkv_path):
    result = subprocess.run(["mkvmerge", "-J", mkv_path], capture_output=True, text=True)
    return json.loads(result.stdout)

def get_audio_bitrates_with_mediainfo(mkv_path):
    """Retourne un dictionnaire {track_id: bitrate} pour chaque piste audio via MediaInfo."""
    bitrates = {}
    result = subprocess.run(["mediainfo", "--Output=JSON", mkv_path], capture_output=True, text=True)
    if result.returncode != 0:
        return bitrates
    data = json.loads(result.stdout)
    tracks = data.get("media", {}).get("track", [])
    audio_idx = 0
    for t in tracks:
        if t.get("@type") == "Audio":
            # On suppose que l'ordre des pistes audio dans MediaInfo == mkvmerge
            br = t.get("BitRate") or t.get("BitRate_Nominal")
            try:
                br = int(br)
            except (TypeError, ValueError):
                br = 0
            bitrates[audio_idx] = br
            audio_idx += 1
    return bitrates

def filter_tracks(mkv_input, mkv_output):
    info = get_track_info(mkv_input)
    tracks = info["tracks"]
    # Récupère les bitrates réels via MediaInfo
    audio_bitrates = get_audio_bitrates_with_mediainfo(mkv_input)

    best_vf, best_vo, fr_subs = None, None, []

    for t in tracks:
        if t["type"] == "audio":
            lang = t.get("properties", {}).get("language", "")
            # Utilise le bitrate MediaInfo si dispo, sinon 0
            track_idx = t["id"]
            br = audio_bitrates.get(track_idx, 0)
            if lang.startswith("fr") and (not best_vf or br > audio_bitrates.get(best_vf["id"], 0)):
                best_vf = t
            elif lang.startswith("en") and (not best_vo or br > audio_bitrates.get(best_vo["id"], 0)):
                best_vo = t
        elif t["type"] == "subtitles" and t.get("properties", {}).get("language", "").startswith("fr"):
            fr_subs.append(t)

    args = ["mkvmerge", "-o", mkv_output]
    
    # Ajouter la piste vidéo
    args.extend(["--video-tracks", "0"])
    
    # Ajouter les pistes audio sélectionnées
    if best_vf:
        args.extend(["--audio-tracks", str(best_vf["id"])])
    if best_vo:
        args.extend(["--audio-tracks", str(best_vo["id"])])
    
    # Ajouter les sous-titres français
    if fr_subs:
        sub_ids = [str(s["id"]) for s in fr_subs]
        args.extend(["--subtitle-tracks", ",".join(sub_ids)])
    
    args.append(mkv_input)
    subprocess.run(args, check=True)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 track_filter.py <input_mkv> <output_mkv>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist")
        sys.exit(1)
    
    try:
        filter_tracks(input_file, output_file)
        print(f"Successfully filtered tracks. Output saved to {output_file}")
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        sys.exit(1)
