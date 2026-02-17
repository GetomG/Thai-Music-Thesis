# notation_utils.py
# -----------------------------------------------------------
# Universal Thai symbolic notation utilities
# Instrument-agnostic
# Used for:
# - MIDI rendering
# - Feature extraction
# - LSTM / Transformer generation
# - Tokenization
# -----------------------------------------------------------

import re

THAI_NOTES = "ดรมฟซลท"
LOW_DOT = "\u0E3A"   # ฺ
HIGH_DOT = "ํ"


# -----------------------------------------------------------
# 1) Flatten JSON notation (supports old + new formats)
# -----------------------------------------------------------
def flatten_song_notation(song_data):
    """
    Returns a flat list of tokens in time order.
    Handles:
      - normal bar lists
      - new format [{"นำ":[...]}, {"ตาม":[...]}]
      - old dict format {"นำ":[...], "ตาม":[...]}
    """
    notation = []

    for sec in song_data.get("sections", []):
        for bar in sec.get("bars", []):

            # Case 1: bar is list
            if isinstance(bar, list):
                for item in bar:
                    if isinstance(item, str):
                        notation.append(item)

                    elif isinstance(item, dict):
                        for _, v in item.items():
                            if isinstance(v, list):
                                notation.extend(v)
                            else:
                                notation.append(v)

            # Case 2: bar is dict
            elif isinstance(bar, dict):
                for key in ["นำ", "ตาม"]:
                    if key in bar:
                        notation.extend(bar[key])

    return notation


# -----------------------------------------------------------
# 2) Convert low / high dot markers into numeric octave tags
#    ฺ  → 1
#    (none) → 2
#    ํ  → 3
# -----------------------------------------------------------
def convert_low_notes(seq):
    return re.sub(
        rf"([ดรมฟซลท]){LOW_DOT}+",
        lambda m: m.group(1) + "1",
        seq
    )


def convert_high_notes(seq):
    return re.sub(
        r"([ดรมฟซลท])ํ",
        lambda m: m.group(1) + "3",
        seq
    )


def normalize_octave_markers(sequence):
    """
    Convert Thai dot markers into numeric octave tags.
    Must run low conversion first.
    """
    sequence = convert_low_notes(sequence)
    sequence = convert_high_notes(sequence)
    return sequence


# -----------------------------------------------------------
# 3) Merge tokens into continuous string
# -----------------------------------------------------------
def notation_to_sequence(notation_tokens):
    """
    Merge list of slot tokens into single continuous sequence string.
    """
    return "".join(notation_tokens)