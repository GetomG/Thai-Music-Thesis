# midi_ranad.py
# -----------------------------------------------------------
# Ranad MIDI Renderer
# Includes:
# - octave pairing
# - กรอ (roll) logic
# - ranad tuning & brightness
# -----------------------------------------------------------

import random
import re
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo


# -----------------------------------------------------------
# Thai pitch mapping (Ranad tuning base)
# -----------------------------------------------------------
THAI_BASE = {
    'ด': 58,
    'ร': 60,
    'ม': 62,
    'ฟ': 63,
    'ซ': 65,
    'ล': 67,
    'ท': 69
}

OCTAVE_OFFSET = {
    1: -12,
    2: 0,
    3: +12
}


# -----------------------------------------------------------
# Main MIDI generator
# -----------------------------------------------------------
def generate_ranad_midi(
    sequence,
    output_path,
    bpm=150,
    global_transpose=12,
    play_in_octave_pairs=True,
    enable_roll=True
):
    """
    sequence: string of Thai notes with octave digits (e.g. ด3ร2ม2-)
    output_path: where to save .mid file
    """

    midi = MidiFile(ticks_per_beat=480)
    track = MidiTrack()
    midi.tracks.append(track)

    # Setup
    track.append(MetaMessage('set_tempo', tempo=bpm2tempo(bpm), time=0))
    track.append(MetaMessage('time_signature', numerator=4, denominator=4, time=0))
    track.append(Message('program_change', program=12, time=0))  # Marimba-like

    ticks_per_slot = 240
    breath_gap = ticks_per_slot // 8

    note_pattern = re.compile(r'([ดรมฟซลท])(\d)?')

    cursor = 0
    last_end = 0

    for match in re.finditer(note_pattern, sequence):
        start_idx = match.start()
        symbol, octave_tag = match.groups()

        # silent dashes before note
        dashes_between = sequence[last_end:start_idx].count('-')
        cursor += dashes_between * ticks_per_slot

        octave = int(octave_tag) if octave_tag else 2
        base_pitch = THAI_BASE[symbol]
        main_pitch = base_pitch + OCTAVE_OFFSET[octave] + global_transpose

        pitches = [main_pitch]

        if play_in_octave_pairs:
            pair = main_pitch - 12
            pitches = sorted({main_pitch, pair})

        # count trailing dashes
        j = match.end()
        dash_count = 0
        while j < len(sequence) and sequence[j] == '-':
            dash_count += 1
            j += 1

        # ---------------------------------------
        # กรอ (roll effect)
        # ---------------------------------------
        if enable_roll and dash_count >= 2:
            roll_duration = ticks_per_slot
            roll_step = ticks_per_slot // 4
            elapsed = 0
            toggle = 0

            while elapsed < roll_duration:
                p = pitches[toggle % len(pitches)]
                vel = random.choice([76, 80, 84])
                t = cursor if elapsed == 0 else roll_step

                track.append(Message("note_on", note=p, velocity=vel, time=t))
                track.append(Message("note_off", note=p, velocity=vel, time=roll_step))

                cursor = 0
                elapsed += roll_step
                toggle += 1

            cursor += (dash_count - 1) * ticks_per_slot + breath_gap
            last_end = j
            continue

        # ---------------------------------------
        # Normal note
        # ---------------------------------------
        track.append(Message("note_on", note=pitches[0], velocity=80, time=cursor))
        for p in pitches[1:]:
            track.append(Message("note_on", note=p, velocity=80, time=0))

        track.append(Message("note_off", note=pitches[0], velocity=80, time=ticks_per_slot))
        for p in pitches[1:]:
            track.append(Message("note_off", note=p, velocity=80, time=0))

        cursor = 0
        cursor += dash_count * ticks_per_slot
        last_end = j

    # remaining silence
    cursor += sequence[last_end:].count('-') * ticks_per_slot
    track.append(MetaMessage("end_of_track", time=cursor))

    midi.save(output_path)