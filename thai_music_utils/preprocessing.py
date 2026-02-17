# preprocessing.py

import copy
import re

def flatten_song_data(nested_song_data):
    flat_data = {
        "title": nested_song_data.get("title", "Untitled"),
        "sections": []
    }

    for top_level_sec in nested_song_data.get("sections", []):
        if "bars" in top_level_sec:
            flat_data["sections"].append(top_level_sec)
        elif "sections" in top_level_sec:
            for sub_sec in top_level_sec["sections"]:
                new_sec_name = f"{top_level_sec['name']} {sub_sec.get('name', '')}".strip()
                flat_data["sections"].append({
                    "name": new_sec_name,
                    "bars": sub_sec.get("bars", [])
                })

    return flat_data


def remove_all_signs(song_data):
    data = copy.deepcopy(song_data)
    pattern = re.compile(r"[0-9ํฺ]")

    for sec in data.get("sections", []):
        new_bars = []
        for bar in sec.get("bars", []):
            if isinstance(bar, list):
                new_bar = [pattern.sub("", token) for token in bar]
                new_bars.append(new_bar)

            elif isinstance(bar, dict):
                new_bar = {}
                if "นำ" in bar:
                    new_bar["นำ"] = [pattern.sub("", t) for t in bar["นำ"]]
                if "ตาม" in bar:
                    new_bar["ตาม"] = [pattern.sub("", t) for t in bar["ตาม"]]
                new_bars.append(new_bar)
            else:
                new_bars.append(bar)

        sec["bars"] = new_bars

    return data