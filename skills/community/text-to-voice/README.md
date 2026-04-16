# Text-to-Voice

Convert text to speech using Kyutai's Pocket TTS. Includes usage examples for the CLI and Python API, plus voice cloning tips.

## Requirements

- Python 3.10+
- PyTorch 2.5+

## Install

```bash
pip install pocket-tts
```

## CLI Usage

```bash
# Generate with defaults
uvx pocket-tts generate

# Specify text and output file
pocket-tts generate --text "Hello" --output-path ./audio/hello.wav

# Pick a pre-made voice
pocket-tts generate --voice alba --text "Hello"

# Voice cloning from a local sample
pocket-tts generate --voice ./my_voice.wav --text "Hello"
```

## Python API

```python
from pocket_tts import TTSModel
import scipy.io.wavfile

tts_model = TTSModel.load_model()
voice_state = tts_model.get_state_for_audio_prompt("alba")
audio = tts_model.generate_audio(voice_state, "Hello world!")

scipy.io.wavfile.write("./audio/output.wav", tts_model.sample_rate, audio.numpy())
```

## Voices

Pre-made voices include `alba`, `marius`, `javert`, `jean`, `fantine`, `cosette`, `eponine`, `azelma`.

See [references/voices.md](references/voices.md) for the full catalog and voice URL formats.

## Skill Metadata

The Agent Skill definition lives in [SKILL.md](SKILL.md).
