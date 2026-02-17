# ============================================================
# EDA – Symbolic Statistics
# ------------------------------------------------------------
# Pitch extraction + motif-level pitch statistics
# ============================================================

from collections import Counter
import pandas as pd

from .eda_symbolic_normalization import THAI_NOTES, UP_MARK, LOW_MARK


# ----------------------------
# Extract pitch symbols
# ----------------------------
def extract_symbols(sequence, strip_octave=False):
    """
    Extract note symbols from normalized sequence.

    strip_octave=True:
        Remove ฺ / ํ markers
    """

    symbols = []

    for tok in sequence:
        if tok == "----":
            continue

        i = 0
        while i < len(tok):
            ch = tok[i]

            if ch in THAI_NOTES:
                # attach octave mark if present
                if i + 1 < len(tok) and tok[i + 1] in {UP_MARK, LOW_MARK}:
                    sym = ch + tok[i + 1]
                    i += 2
                else:
                    sym = ch
                    i += 1

                if strip_octave:
                    sym = sym.replace(UP_MARK, "").replace(LOW_MARK, "")

                symbols.append(sym)
            else:
                i += 1

    return symbols


# ----------------------------
# Pitch stats per motif
# ----------------------------
def pitch_stats(songs, strip_octave=False):
    """
    Input:
        songs = list of song dicts
        Each song must have:
            - "motif"
            - "sequence" (normalized)

    Output:
        dict: { motif -> Counter }
    """

    stats = {}

    for motif in {s["motif"] for s in songs}:
        counter = Counter(
            sym
            for s in songs if s["motif"] == motif
            for sym in extract_symbols(s["sequence"], strip_octave)
        )
        stats[motif] = counter

    return stats


# ----------------------------
# Convert stats → DataFrame
# ----------------------------
def stats_to_df(stats_by_motif):
    """
    Convert motif pitch stats into per-motif DataFrames.
    """

    dfs = {}

    for motif, counter in stats_by_motif.items():
        total = sum(counter.values())

        df = (
            pd.DataFrame([
                {
                    "note": note,
                    "count": cnt,
                    "percent": cnt / total * 100 if total else 0
                }
                for note, cnt in counter.items()
            ])
            .sort_values("count", ascending=False)
            .reset_index(drop=True)
        )

        dfs[motif] = df

    return dfs