"""
octave_inference.py

Utilities for:
- Thai note octave inference (DP-based)
- Respecting existing octave labels
- Injecting inferred octave markers (ฺ / ํ)
"""

import copy

# -------------------------------------------------------
# Core Definitions
# -------------------------------------------------------

THAI_NOTES = "ดรมฟซลท"

LOW_DOT = "ฺ"   # octave 1
HIGH_DOT = "ํ"  # octave 3

thai_base = {
    'ด': 58,
    'ร': 60,
    'ม': 62,
    'ฟ': 63,
    'ซ': 65,
    'ล': 67,
    'ท': 69
}

octave_offset = {
    1: -12,
    2: 0,
    3: 12
}

# Allowed octave constraints (musically valid only)
allowed_oct = {
    'ด': [2, 3],
    'ร': [2, 3],
    'ม': [2, 3],
    'ฟ': [2, 3],
    'ซ': [1, 2, 3],
    'ล': [1, 2, 3],
    'ท': [1, 2],  # no ทํ
}


# -------------------------------------------------------
# Utility helpers
# -------------------------------------------------------

def is_thai_note(ch):
    return ch in THAI_NOTES


def get_fixed_octave(token, i):
    """
    Detect explicit octave marker after Thai note.
    Returns 1 / 2 / 3 or None.
    """
    if i + 1 >= len(token):
        return None

    nxt = token[i + 1]

    if nxt == LOW_DOT:
        return 1
    if nxt == HIGH_DOT:
        return 3
    if nxt.isdigit() and nxt in "123":
        return int(nxt)

    return None


# -------------------------------------------------------
# Dynamic Programming Octave Inference
# -------------------------------------------------------

def guess_octaves_with_constraints(
    notes,
    fixed_octaves,
    prefer_octave=2,
    low_pitch=58 - 12,
    high_pitch=69 + 12,
    max_jump=4
):
    """
    Infer octave sequence using DP smoothness constraint.
    """

    N = len(notes)
    if N == 0:
        return []

    INF = 10**9

    dp = [[INF] * 4 for _ in range(N)]
    prev = [[None] * 4 for _ in range(N)]

    def pitch(note, octv):
        return thai_base[note] + octave_offset[octv]

    def range_penalty(p):
        if p < low_pitch or p > high_pitch:
            return 10 + 0.5 * min(abs(p - low_pitch), abs(p - high_pitch))
        return 0.0

    # ---- init first note ----
    n0 = notes[0]
    fixed0 = fixed_octaves[0]
    allowed0 = allowed_oct.get(n0, [prefer_octave])

    for o in allowed0:
        if fixed0 is not None and o != fixed0:
            continue

        p0 = pitch(n0, o)
        cost = abs(o - prefer_octave) + range_penalty(p0)

        dp[0][o] = cost
        prev[0][o] = None

    # ---- transitions ----
    for i in range(1, N):
        n_prev = notes[i - 1]
        n_cur = notes[i]
        fixed_i = fixed_octaves[i]

        allowed_cur = allowed_oct.get(n_cur, [prefer_octave])

        for o_cur in allowed_cur:
            if fixed_i is not None and o_cur != fixed_i:
                continue

            p_cur = pitch(n_cur, o_cur)
            rp = range_penalty(p_cur)

            best_cost = INF
            best_prev = None

            for o_prev in [1, 2, 3]:
                if dp[i - 1][o_prev] >= INF:
                    continue

                p_prev = pitch(n_prev, o_prev)
                base_cost = dp[i - 1][o_prev]

                interval = abs(p_cur - p_prev)

                if interval <= max_jump:
                    jump_cost = interval * 0.5
                elif interval <= 7:
                    jump_cost = 2 + (interval - max_jump)
                else:
                    jump_cost = 10 + (interval - 7) * 2

                octave_switch = 0 if o_cur == o_prev else 1.5

                total = base_cost + jump_cost + octave_switch + rp

                if total < best_cost:
                    best_cost = total
                    best_prev = o_prev

            dp[i][o_cur] = best_cost
            prev[i][o_cur] = best_prev

    # ---- backtrack ----
    last_note = notes[-1]
    allowed_last = allowed_oct.get(last_note, [prefer_octave])

    best_last = min(allowed_last, key=lambda o: dp[N - 1][o])

    tags = [0] * N
    tags[N - 1] = best_last

    for i in range(N - 1, 0, -1):
        tags[i - 1] = prev[i][tags[i]]

    # Enforce fixed octaves again (safety)
    for i, fo in enumerate(fixed_octaves):
        if fo is not None:
            tags[i] = fo

    return tags


# -------------------------------------------------------
# Main API
# -------------------------------------------------------

def add_octaves_respecting_labels(song_data):
    """
    Apply DP octave inference while respecting
    existing explicit octave labels.
    """

    data = copy.deepcopy(song_data)

    notes = []
    fixed_octaves = []

    # ---- Collect notes ----
    for sec in data["sections"]:
        for bar in sec["bars"]:
            token_lists = []

            if isinstance(bar, list):
                token_lists = [bar]
            elif isinstance(bar, dict):
                token_lists = [bar.get("นำ", []), bar.get("ตาม", [])]

            for tokens in token_lists:
                for token in tokens:
                    i = 0
                    while i < len(token):
                        ch = token[i]
                        if is_thai_note(ch):
                            fo = get_fixed_octave(token, i)
                            notes.append(ch)
                            fixed_octaves.append(fo)
                        i += 1

    if not notes:
        return data

    tags = guess_octaves_with_constraints(notes, fixed_octaves)
    idx = 0

    # ---- Inject inferred markers ----
    for sec in data["sections"]:
        for bi, bar in enumerate(sec["bars"]):

            token_lists = []
            dict_mode = False

            if isinstance(bar, list):
                token_lists = [bar]
            elif isinstance(bar, dict):
                token_lists = [bar.get("นำ", []), bar.get("ตาม", [])]
                dict_mode = True

            for tl_i, tokens in enumerate(token_lists):
                new_tokens = []

                for token in tokens:
                    new_chars = []
                    i = 0

                    while i < len(token):
                        ch = token[i]
                        new_chars.append(ch)

                        if is_thai_note(ch):
                            fo = get_fixed_octave(token, i)
                            tag_oct = tags[idx]
                            idx += 1

                            if fo is None:
                                if tag_oct == 1:
                                    new_chars.append(LOW_DOT)
                                elif tag_oct == 3:
                                    new_chars.append(HIGH_DOT)

                        i += 1

                    new_tokens.append("".join(new_chars))

                if not dict_mode:
                    sec["bars"][bi] = new_tokens
                else:
                    if tl_i == 0:
                        bar["นำ"] = new_tokens
                    else:
                        bar["ตาม"] = new_tokens

    return data