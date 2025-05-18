import subprocess
import json
from language_map import get_iso1, get_full_name

def run_mediainfo(file_path: str) -> dict:
    result = subprocess.run(
        ["mediainfo", "--Output=JSON", file_path],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

def parse_tracks(mediainfo_data: dict) -> list:
    return mediainfo_data["media"]["track"]

def extract_audio_tracks(tracks: list) -> list:
    return [
        t for t in tracks if t["@type"] == "Audio"
    ]

def extract_subtitle_tracks(tracks: list) -> list:
    return [
        t for t in tracks if t["@type"] == "Text" or t["@type"] == "Subtitle"
    ]

def extract_video_track(tracks: list) -> dict:
    for t in tracks:
        if t["@type"] == "Video":
            return t
    return {}

def get_audio_info(track: dict) -> dict:
    lang_raw = track.get("Language", "und")
    lang_code = get_iso1(lang_raw)
    lang_name = get_full_name(lang_code)
    codec = track.get("Format", "Unknown")
    channels = track.get("Channel(s)_Original", track.get("Channel(s)", "Unknown"))
    bitrate = track.get("BitRate", None)

    # Bitrate en kbps si disponible
    if bitrate:
        bitrate_kbps = round(int(bitrate) / 1000)
        bitrate_str = f"{bitrate_kbps} kbps"
    else:
        bitrate_str = "Unknown bitrate"

    return {
        "language_code": lang_code,
        "language_name": lang_name,
        "codec": codec,
        "channels": channels,
        "bitrate": bitrate_str
    }

def get_subtitle_info(track: dict, kbps_list: list) -> dict:
    lang_raw = track.get("Language", "und")
    lang_code = get_iso1(lang_raw)
    lang_name = get_full_name(lang_code)
    kbps = float(track.get("BitRate", 0)) / 1000

    # Détermination des types selon le débit
    if not kbps_list:
        subtitle_type = "UNKNOWN"
    else:
        sorted_kbps = sorted(kbps_list)
        if kbps == sorted_kbps[0]:
            subtitle_type = "FR FORCED"
        elif len(sorted_kbps) >= 3 and kbps == sorted_kbps[-1]:
            subtitle_type = "FR SDH"
        else:
            subtitle_type = "FR FULL"

    return {
        "language_code": lang_code,
        "language_name": lang_name,
        "bitrate": round(kbps, 3),
        "title": subtitle_type
    }

def get_french_subtitle_kbps(tracks: list) -> list:
    french_kbps = []
    for t in tracks:
        lang = get_iso1(t.get("Language", "und"))
        if lang == "fr":
            bitrate = t.get("BitRate", 0)
            kbps = float(bitrate) / 1000 if bitrate else 0
            french_kbps.append(kbps)
    return french_kbps
