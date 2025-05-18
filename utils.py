import os

def get_source_url(source_path):
    if os.path.isfile(source_path) and source_path.endswith(".iso"):
        return f"iso://{source_path}"
    elif os.path.isdir(source_path):
        if "BDMV" in os.listdir(source_path):
            return f"file://{source_path}"
        elif os.path.basename(source_path).upper() == "BDMV":
            return f"file://{os.path.dirname(source_path)}"
    raise ValueError("Format non pris en charge.")

def get_playlist_folder(source_path):
    if os.path.basename(source_path).upper() == "BDMV":
        return os.path.join(source_path, "PLAYLIST")
    return os.path.join(source_path, "BDMV", "PLAYLIST")
