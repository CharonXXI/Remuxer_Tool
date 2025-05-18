import subprocess
import re
import os

MAKEMKV_PATH = "/Applications/MakeMKV.app/Contents/MacOS/makemkvcon"

def get_makemkv_info(source_url):
    result = subprocess.run([MAKEMKV_PATH, "-r", "info", source_url], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError("Erreur MakeMKV info")
    return result.stdout

def parse_title_durations(info_text):
    durations = {}
    current_title = None
    for line in info_text.splitlines():
        # Cherche le début d'un nouveau titre
        title_match = re.match(r'TINFO:(\d+),2,0,"([^"]+)"', line)
        if title_match:
            current_title = int(title_match.group(1))
            continue
            
        # Cherche la durée du titre
        if current_title is not None:
            duration_match = re.match(r'TINFO:' + str(current_title) + r',9,0,"(\d+):(\d+):(\d+)"', line)
            if duration_match:
                h, m, s = map(int, duration_match.groups())
                durations[current_title] = h * 3600 + m * 60 + s
                current_title = None
    return durations

def extract_title(source_url, title_id, output_dir):
    subprocess.run([MAKEMKV_PATH, "mkv", source_url, str(title_id), output_dir], check=True)
