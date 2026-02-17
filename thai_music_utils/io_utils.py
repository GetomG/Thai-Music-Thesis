# io_utils.py
import json

def save_json_bar_per_line(data, path):
    """Pretty-print JSON but keep each bar (list) on one line."""
    raw = json.dumps(data, ensure_ascii=False, indent=2)
    lines = raw.split("\n")
    out = []
    inside_bar = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("[") and '"' in stripped and stripped.endswith("],"):
            out.append(line)
            continue

        if stripped.startswith("[") and not stripped.startswith("[{"):
            inside_bar = True
            out.append(line.rstrip())
            continue

        if inside_bar:
            out[-1] += " " + stripped
            if stripped.endswith("],") or stripped.endswith("]"):
                inside_bar = False
            continue

        out.append(line)

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
