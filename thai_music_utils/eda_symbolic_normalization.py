# ============================================================
# EDA – Symbolic Normalization
# ------------------------------------------------------------
# Purpose:
# - Standardize Thai classical symbolic notation
# - Preserve musical meaning (notes + register)
# - Do NOT infer octave or fix musical structure
# ============================================================

# ----------------------------
# Allowed symbolic vocabulary
# ----------------------------
THAI_NOTES = set("ดรมฟซลท")
UP_MARK = "ํ"     # upper register
LOW_MARK = "ฺ"    # lower register
REST_TOKEN = "----"


# ----------------------------
# Helper: detect rest token
# ----------------------------
def is_rest(token):
    """
    True if token consists only of '-' characters.
    """
    return isinstance(token, str) and len(token) > 0 and all(ch == "-" for ch in token)


# ----------------------------
# Normalize ONE symbolic token
# ----------------------------
def normalize_token(token):
    """
    Input:
        Raw token from JSON / OCR

    Output:
        - Valid Thai note (with register preserved)
        - OR unified rest token "----"
    """

    if not isinstance(token, str):
        return REST_TOKEN

    token = token.strip()

    if is_rest(token):
        return REST_TOKEN

    out = []
    for ch in token:
        if ch in THAI_NOTES or ch in {UP_MARK, LOW_MARK}:
            out.append(ch)

    return "".join(out) if out else REST_TOKEN


# ----------------------------
# Normalize ONE bar
# ----------------------------
def normalize_bar(bar):
    return [normalize_token(tok) for tok in bar]


# ----------------------------
# Flatten full song → token sequence
# ----------------------------
def flatten_song(song_json):
    """
    Input:
        Full song JSON with sections + bars

    Output:
        One long normalized token list
    """

    sequence = []

    for section in song_json.get("sections", []):
        for bar in section.get("bars", []):
            if isinstance(bar, list):
                sequence.extend(normalize_bar(bar))
            elif isinstance(bar, dict):
                # Handle นำ / ตาม format
                for key in ["นำ", "ตาม"]:
                    if key in bar:
                        sequence.extend(normalize_bar(bar[key]))

    return sequence