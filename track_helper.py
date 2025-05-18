from mediainfo_helper import (
    run_mediainfo,
    parse_tracks,
    extract_audio_tracks,
    extract_subtitle_tracks,
    extract_video_track,
    get_audio_info,
    get_subtitle_info,
    get_french_subtitle_kbps
)

VF_TAGS = ["VFF", "VFQ", "VFi", "VOF"]

def select_video_track(file_path):
    mediainfo = run_mediainfo(file_path)
    tracks = parse_tracks(mediainfo)
    return extract_video_track(tracks)

def select_audio_tracks(file_path):
    mediainfo = run_mediainfo(file_path)
    tracks = parse_tracks(mediainfo)
    audio_tracks = extract_audio_tracks(tracks)

    best_vo = None
    best_vf = None
    best_vo_bitrate = 0
    best_vf_bitrate = 0

    for track in audio_tracks:
        info = get_audio_info(track)
        lang = info["language_code"]
        bitrate = int(info["bitrate"].split()[0]) if info["bitrate"] != "Unknown bitrate" else 0

        if lang == "en" and bitrate > best_vo_bitrate:
            best_vo = {**track, "info": info}
            best_vo_bitrate = bitrate

        if lang == "fr" and bitrate > best_vf_bitrate:
            best_vf = {**track, "info": info}
            best_vf_bitrate = bitrate

    return best_vo, best_vf

def select_subtitle_tracks(file_path):
    mediainfo = run_mediainfo(file_path)
    tracks = parse_tracks(mediainfo)
    subtitle_tracks = extract_subtitle_tracks(tracks)
    fr_kbps_list = get_french_subtitle_kbps(subtitle_tracks)

    fr_subs = []
    for track in subtitle_tracks:
        lang = track.get("Language", "und").lower()
        if lang in ["fre", "fr", "french"]:
            info = get_subtitle_info(track, fr_kbps_list)
            fr_subs.append({**track, "info": info})
    return fr_subs
