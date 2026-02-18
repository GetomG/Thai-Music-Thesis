# Thai Classical Music Generation & Analysis

A comprehensive research project on Thai classical music generation using deep learning and symbolic music representation. This repository contains data processing pipelines, music analysis utilities, and neural network models for generating and understanding Thai classical music compositions.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Dataset Structure](#dataset-structure)
3. [Workflow & Notebooks](#workflow--notebooks)
4. [Utility Modules](#utility-modules)
5. [Installation & Setup](#installation--setup)
6. [Usage Examples](#usage-examples)
7. [Project Architecture](#project-architecture)
8. [Key Concepts](#key-concepts)

---

## Project Overview

This project aims to:

- **Digitize Thai Classical Music**: Convert handwritten Thai music notation into symbolic JSON format using OCR (PaddleOCR)
- **Normalize & Standardize**: Process raw symbolic data into clean, consistent representations suitable for machine learning
- **Generate New Compositions**: Train baseline LSTM language models to generate authentic Thai music sequences
- **Analyze Musical Patterns**: Extract and analyze patterns in Thai classical music (motifs, phrases, intervals, etc.)

### Key Features

- **Multi-motif Dataset**: ~100 Thai classical songs across 60+ musical motifs (ลาว, เขมร, พม่า, ญวน, จีน, etc.)
- **Octave Inference**: Dynamic programming approach to infer musical octaves from symbolic constraints
- **Symbolic Tokenization**: Convert Thai musical notation into token sequences for sequence modeling
- **MIDI Integration**: Generate playable MIDI files with Ranad (Thai xylophone) instrument configurations
- **Exploratory Data Analysis**: Statistical analysis and visualization of musical patterns

---

## Dataset Structure

```
thai_music_data/
├── songs/                           # Main dataset organized by motif
│   ├── ลาว/                        # Motif directory (Thai names)
│   │   ├── ลาวกระทบไม้/
│   │   │   ├── json/               # Cleaned symbolic notation
│   │   │   ├── meta/               # Metadata files
│   │   │   ├── midi/               # Generated MIDI
│   │   │   └── raw/                # Raw input files
│   │   ├── ลาวเจริญศรี/
│   │   └── ...
│   │
│   ├── เขมร/                        # Khmer motif
│   ├── พม่า/                        # Burmese motif
│   ├── จีน/                         # Chinese motif
│   ├── ญวน/                         # Vietnamese motif
│   └── ...                          # 10+ motif folders
│
├── weights/                         # Trained model weights
├── raw/                             # Raw OCR input (if available)
└── Thai music metadata (best).pdf   # Reference documentation
```

### JSON Format

Each song is stored as a structured JSON file with the following schema:

```json
{
  "title": "แขกกุลิต(แขกหนัง)เถา",
  "sections": [
    {
      "name": "สามชั้น เที่ยวแรก",
      "bars": [
        [ "---ร", "---ซ", "---ล", "---ท", "-ดํ-รํ", "มํรํดํท", "ลซลท", "-ดํ-รํ" ],
        [ "---ซํ", "---มํ", "---รํ", "---ดํ", "--รํมํ", "รํดํทรํ", "ดํทลดํ", "ทลซล" ],
        [ "--รซ", "ลทดํรํ", "----", "มํรํซํมํ", "---รํ", "ดํมํรํดํ", "--รํมํ", "รํดํทล" ],
        [ "----", "ดํลซฟ", "ซฟดฟ", "-ซ-ล", "--ซดํ", "----", "ซลดํล", "ซฟ-ซ" ],
        [ "ลทดํรํ", "----", "มํรํดํล", "----", "ดํลซฟ", "มรดร", "มฟซล", "----" ],
        [ "ลทดํรํ", "----", "มํรํดํล", "----", "----", "ดํฟซล", "ดํลซล", "ซฟมฟ" ],
        [ "--มร", "----", "รดรม", "ฟมซฟ", "----", "ดฟซล", "-ลท-", "ลทซล" ],
        [ "----", "----", "ทลซดํ", "-ท-ล", "ทลซดํ", "-ท-ล", "ซลดํล", "ซฟ-ซ" ]
      ]
    }
```

**Notation:**
- **Thai notes**: ด ร ม ฟ ซ ล ท (7 notes, similar to C D E F G A B)
- **Dashes (-)**: Rests/pauses
- **Thai dots**:
  - `ฺ` (LOW_DOT): Lower octave (octave 1)
  - (none): Middle octave (octave 2, default)
  - `ํ` (HIGH_DOT): Upper octave (octave 3)
- **Bars**: Organized by section → bar → token sequences
- **Slots**: Can be simple strings or complex objects with lead/accompaniment (นำ/ตาม)

---

## Workflow & Notebooks

The project follows a three-stage pipeline:

### 1. **Thai_Classical_note_Intake.ipynb** (Stage 1: Data Ingestion)

**Purpose**: Extract and clean Thai music notation from raw sources

**Key Tasks**:
- Load raw symbolic notation files
- Parse and validate JSON format
- Handle multi-part structures (lead/accompaniment)
- Basic octave inference and note validation
- Export cleaned JSON files to standardized format

**Inputs**: Raw song notation files  
**Outputs**: Cleaned JSON in `thai_music_data/songs/<motif>/<song>/json/`

### 2. **Phrase_1_Experiments.ipynb** (Stage 2: Exploratory Data Analysis)

**Purpose**: Analyze musical patterns and extract statistical insights

**Key Tasks**:
- Extract and analyze musical motifs/phrases
- Compute n-gram statistics (bigrams, trigrams, quadgrams)
- Perform similarity analysis between motifs
- Visualize pitch distributions and intervals
- Test different tokenization strategies
- Develop baseline metrics for music generation quality

**Analysis Types**:
- **Pitch Analysis**: Histogram of note frequencies, octave distribution
- **Interval Analysis**: Distribution of pitch jumps/steps
- **N-gram Analysis**: Most common 2-grams, 3-grams, 4-grams by motif
- **Similarity**: Compute similarity matrices between motif phrase vectors

**Outputs**: Statistical tables, visualizations, baseline metrics

### 3. **New_Stage3_Generation_Baseline_LSTM_structured.ipynb** (Stage 3: Model Training & Generation)

**Purpose**: Train baseline LSTM language model for music generation

**Key Tasks**:
- Load normalized symbolic sequences from Stage 1
- Build vocabulary from pitch tokens and rest tokens
- Prepare training/validation datasets
- Define and train conditional LSTM model
- Generate new music sequences
- Evaluate model performance

**Model Architecture**:
- Input: Flattened token sequences per song
- Encoding: Token embedding layer
- Core: Stacked LSTM cells (bidirectional optional)
- Output: Softmax classification over vocabulary
- Loss: Cross-entropy on next-token prediction

**Inputs**: Cleaned JSON files from Stage 1  
**Outputs**: Trained model weights, generated sequences, evaluation metrics

**Key Functions Used**:
- `eda_symbolic_normalization.normalize_token()`: Standardize individual tokens
- `eda_symbolic_normalization.flatten_song()`: Convert full song to token list
- `preprocessing.flatten_song_data()`: Handle nested structures
- MIDI rendering for audio playback

---


## Utility Modules

Located in `thai_music_utils/`:

### 1. **constants.py**
Defines fundamental Thai musical constants and mappings.

```python
THAI_NOTES = "ดรมฟซลท"           # 7-note scale
thai_base = {                      # MIDI pitch mappings
    'ด': 58, 'ร': 60, 'ม': 62,
    'ฟ': 63, 'ซ': 65, 'ล': 67, 'ท': 69
}
octave_offset = {
    1: -12,  # Lower octave
    2: 0,    # Middle octave (base)
    3: 12    # Upper octave
}
allowed_oct = {  # Valid octaves per note
    'ด': [2, 3], 'ร': [2, 3], 'ม': [2, 3],
    'ฟ': [2, 3], 'ซ': [1, 2, 3], 'ล': [1, 2, 3], 'ท': [1, 2]
}
```

### 2. **notation_utils.py**
Universal Thai symbolic notation processing (instrument-agnostic).

**Key Functions**:
- `flatten_song_notation(song_data)`: Convert nested JSON to flat token list
- `normalize_octave_markers(sequence)`: Convert Thai dot markers (ฺ/ํ) to numeric octave tags
- `notation_to_sequence(notation_tokens)`: Merge token list into continuous string

### 3. **eda_symbolic_normalization.py**
Standardize and normalize symbolic musical notation.

**Key Functions**:
- `normalize_token(token)`: Clean individual token, preserve register markers
- `normalize_bar(bar)`: Normalize all tokens in a bar
- `flatten_song(song_json)`: Extract full song as normalized token sequence
- `is_rest(token)`: Detect rest/pause tokens

### 4. **octave_inference.py**
Dynamic programming approach to infer musical octaves from symbolic constraints.

**Key Functions**:
- `is_thai_note(ch)`: Check if character is valid Thai note
- `get_fixed_octave(note, label)`: Extract octave from note with dot markers
- `guess_octaves_with_constraints(sequence, allowed_octaves, gap_penalty)`: DP-based octave inference
- `add_octaves_respecting_labels(sequence, allowed_octaves)`: Apply inferred octaves

**Algorithm**: Uses dynamic programming to find smooth octave transitions that minimize jumps while respecting constraints from explicit markers.

### 5. **preprocessing.py**
Data cleaning and structure flattening.

**Key Functions**:
- `flatten_song_data(nested_song_data)`: Flatten hierarchical section/bar structures
- `remove_all_signs(song_data)`: Strip all decorative markers (numbers, dots) to get pitch-only

### 6. **eda_stats.py**
Statistical extraction and analysis.

**Key Functions**:
- `extract_symbols(song_data)`: Get list of all tokens in a song
- `pitch_stats(symbols)`: Compute statistics (mean, std, distribution)
- `stats_to_df(stats_dict)`: Convert statistics to pandas DataFrame

### 7. **io_utils.py**
File I/O and data serialization.

**Key Functions**:
- `save_json_bar_per_line(data, filepath)`: Save JSON with each bar on separate line (for diffs)

### 8. **midi_ranad.py**
MIDI generation with Ranad (Thai xylophone) instrument configuration.

**Key Functions**:
- `generate_ranad_midi(pitch_sequence, output_path, tempo, velocity)`: Generate playable MIDI from pitch sequence
- Handles octave-aware pitch-to-MIDI conversion
- Configures instrument and tempo

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- Jupyter Notebook / JupyterLab
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/GetomG/Thai-Music-Thesis.git
cd Thai-Music-Thesis
```

### Step 2: Install Core Dependencies
```bash
pip install mido python-rtmidi  # MIDI support
pip install tqdm                 # Progress bars
pip install pandas numpy         # Data processing
pip install matplotlib          # Visualization
```

### Step 3: Install OCR (Optional, for Stage 2)
```bash
pip install paddlepaddle==3.2.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
pip install "paddleocr[all]"
```

### Step 4: Thai Font for Visualization (Optional)
```bash
wget https://github.com/Phonbopit/sarabun-webfont/raw/master/fonts/thsarabunnew-webfont.ttf
# Then configure in your notebook/matplotlib
```

### Step 5: Verify Installation
```python
from thai_music_utils.constants import THAI_NOTES
from thai_music_utils.notation_utils import flatten_song_notation
print("✓ Thai Music Utils loaded successfully")
```

---

## Usage Examples

### Example 1: Load and Inspect a Song

```python
import json
from thai_music_utils.notation_utils import flatten_song_notation

# Load song
with open('thai_music_data/songs/ลาว/ลาวกระทบไม้/json/song.json') as f:
    song = json.load(f)

# Flatten to sequence
notation = flatten_song_notation(song)
print(f"Song: {song['title']}")
print(f"Total tokens: {len(notation)}")
print(f"First 10 tokens: {notation[:10]}")
```

### Example 2: Normalize Notation

```python
from thai_music_utils.eda_symbolic_normalization import normalize_token, flatten_song

# Normalize individual tokens
print(normalize_token("ด"))        # 'ด'
print(normalize_token("---"))       # '----'
print(normalize_token("รํ"))        # 'รํ' (with register marker)

# Flatten and normalize full song
with open('thai_music_data/songs/ลาว/ลาวกระทบไม้/json/song.json') as f:
    song = json.load(f)
    
normalized_sequence = flatten_song(song)
print(f"Normalized sequence: {normalized_sequence}")
```

### Example 3: Infer Octaves

```python
from thai_music_utils.octave_inference import guess_octaves_with_constraints
from thai_music_utils.constants import allowed_oct

sequence = "รมฟซลท"  # No octave markers
inferred = guess_octaves_with_constraints(
    sequence, 
    allowed_octaves=allowed_oct,
    gap_penalty=1.0
)
print(f"Original:  {sequence}")
print(f"Inferred:  {inferred}")
```

### Example 4: Generate MIDI

```python
from thai_music_utils.midi_ranad import generate_ranad_midi

# Simple pitch sequence (pitch_class + octave)
pitches = ['ร2', 'ม2', 'ฟ2', 'ซ3', 'ล3', 'ท2']
output_path = 'output.mid'

generate_ranad_midi(
    pitches,
    output_path,
    tempo=120,
    velocity=80
)
print(f"✓ MIDI saved to {output_path}")
```

### Example 5: Train Mini LSTM (Pseudocode)

See `New_Stage3_Generation_Baseline_LSTM_structured.ipynb` for full implementation.

```python
# Load data
songs = load_songs_from_json()  # Returns list of dicts

# Normalize
sequences = [flatten_song(s) for s in songs]

# Build vocabulary
vocab = build_vocab(sequences)

# Prepare dataset
X, y = prepare_sequences(sequences, vocab, seq_length=64)

# Train model
model = build_lstm_model(vocab_size=len(vocab))
model.train(X, y, epochs=50, batch_size=32)

# Generate
new_sequence = model.generate(prompt_tokens=5, length=100)
```

---

## Project Architecture

```
Thai-Music-Thesis/
│
├── README.md                          # This file
│
├── thai_music_utils/                  # Core utility library
│   ├── constants.py
│   ├── notation_utils.py
│   ├── octave_inference.py
│   ├── eda_symbolic_normalization.py
│   ├── preprocessing.py
│   ├── eda_stats.py
│   ├── io_utils.py
│   └── midi_ranad.py
│
├── thai_music_data/                   # Dataset
│   ├── songs/                         # [Organized by motif → song]
│   ├── weights/                       # [Model weights]
│   └── raw/                           # [Raw inputs]
│
└── Notebooks/                         # Stage pipelines
    ├── Thai_Classical_note_Intake (1).ipynb          # Stage 1
    ├── (TO_CLEAN)_Phrase_1_Experiments.ipynb         # Stage 2
    └── New_Stage3_Generation_Baseline_LSTM_structured (1).ipynb  # Stage 3
```

---

## Key Concepts

### Thai Classical Music Scale

The Thai musical scale consists of **7 notes** (diatonic):
- **ด** (D) = 58 (MIDI)
- **ร** (R) = 60 (C in Western)
- **ม** (M) = 62 (D in Western)
- **ฟ** (F) = 63 (D#)
- **ซ** (S) = 65 (E)
- **ล** (L) = 67 (G)
- **ท** (T) = 69 (A)

### Octaves

Three octave registers are used:
1. **Octave 1 (Low)**: Marked with ฺ (LOW_DOT), offset -12 semitones
2. **Octave 2 (Mid)**: Default (no marker), offset 0
3. **Octave 3 (High)**: Marked with ํ (HIGH_DOT), offset +12 semitones

### Rests & Notation

- **-** (dash): Rest/pause in a slot
- **---ด**: 3-beat rest followed by ด note
- **รรร**: Repeated note ร three times
- Bars group tokens (typically 8 tokens per bar)
- Sections organize bars thematically

### Motifs

A **motif** (ลำนำ) is a recurring musical phrase or style pattern. This dataset includes 60+ motifs such as:
- **ลาว** (Lao style)
- **เขมร** (Khmer style)
- **พม่า** (Burmese style)
- **ญวน** (Vietnamese style)
- **จีน** (Chinese style)
- And many more classical Thai forms

---

## Workflow Summary

```
Raw Music Notation
        ↓
[Stage 1: Intake] (Thai_Classical_note_Intake.ipynb)
        ↓
Cleaned JSON (thai_music_data/songs/)
        ↓
[Stage 2: EDA] ((TO_CLEAN)_Phrase_1_Experiments.ipynb)
        ↓
Statistical Analysis & Pattern Insights
        ↓
[Stage 3: Generation] (New_Stage3_Generation_Baseline_LSTM_structured.ipynb)
        ↓
Trained LSTM Model + Generated Sequences
```

---

## Contributing

To extend this project:

1. **Add More Songs**: Place cleaned JSON files in `thai_music_data/songs/<motif>/<song>/json/`
2. **Extend Utilities**: Add functions to `thai_music_utils/` modules
3. **Improve Models**: Enhance LSTM architecture or try attention/transformer models
4. **Analyze Patterns**: Add new analysis to exploratory notebook
5. **Generate MIDI**: Integrate with real-time playback or synthesis

---

## References & Resources

- **Thai Music Theory**: [Thai Classical Music Overview](https://en.wikipedia.org/wiki/Thai_music)
- **MIDI Standard**: [MIDI 1.0 Specification](https://www.midi.org/)
- **PaddleOCR**: [PaddleOCR GitHub](https://github.com/PaddlePaddle/PaddleOCR)
- **Sequence Modeling**: [LSTM Introduction](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)

---

## License

This project is part of academic research. Please cite appropriately if used.

---

## Contact & Attribution

**Author**: Thanakrit (GetomG)  
**Repository**: [Thai-Music-Thesis](https://github.com/GetomG/Thai-Music-Thesis)

For questions or suggestions, please open an issue or contact the project maintainer.

---

**Last Updated**: February 2026  
**Project Status**: Active Research
