import os
import struct

def parse_mpls_duration(file_path):
    with open(file_path, "rb") as f:
        data = f.read()

    playlist_start = struct.unpack(">I", data[8:12])[0] + 12
    num_plays = struct.unpack(">H", data[playlist_start:playlist_start+2])[0]

    total_duration = 0
    for i in range(num_plays):
        entry_start = playlist_start + 2 + i * 12
        if entry_start + 12 > len(data):
            continue
        in_time = struct.unpack(">I", data[entry_start+4:entry_start+8])[0]
        out_time = struct.unpack(">I", data[entry_start+8:entry_start+12])[0]
        total_duration += (out_time - in_time) / 45000.0

    return total_duration

def find_main_mpls(playlist_folder):
    max_duration = 0
    main_mpls = None

    for f in os.listdir(playlist_folder):
        if f.endswith(".mpls"):
            path = os.path.join(playlist_folder, f)
            try:
                duration = parse_mpls_duration(path)
                if duration > max_duration:
                    max_duration = duration
                    main_mpls = path
            except:
                continue

    return main_mpls, max_duration
