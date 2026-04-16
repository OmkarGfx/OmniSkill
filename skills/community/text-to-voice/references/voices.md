# Available Voices

Full catalog at: https://huggingface.co/kyutai/tts-voices

## Pre-made Voices (Shorthand Names)

| Name | Gender | Source | License | HuggingFace Path |
|------|--------|--------|---------|------------------|
| alba | Female | Alba MacKenna | CC BY 4.0 | alba-mackenna/casual.wav |
| marius | Male | Voice Donation | CC0 | voice-donations/Selfie.wav |
| javert | Male | Voice Donation | CC0 | voice-donations/Butter.wav |
| jean | Male | EARS | CC-NC | ears/p010/freeform_speech_01.wav |
| fantine | Female | VCTK | CC BY 4.0 | vctk/p244_023.wav |
| cosette | Female | Expresso | CC-NC | expresso/ex04-ex02_confused_001_channel1_499s.wav |
| eponine | Female | VCTK | CC BY 4.0 | vctk/p262_023.wav |
| azelma | Female | VCTK | CC BY 4.0 | vctk/p303_023.wav |

## Voice Sources

### Alba MacKenna (`alba-mackenna/`)
Voice-acted characters, CC BY 4.0:
- `casual.wav` - Very casual dialogue
- `merchant.wav` - RPG merchant style
- `announcer.wav` - Competitive games announcer

### Voice Donations (`voice-donations/`)
Volunteer recordings, CC0 (public domain). Enhanced versions available as `*_enhanced.wav`.

### VCTK (`vctk/`)
Voice Cloning Toolkit dataset, CC BY 4.0. Multiple speakers with `mic1` recordings.

### Expresso (`expresso/`)
Expressive speech dataset, CC-NC (non-commercial only). Includes emotional variants.

### EARS (`ears/`)
High-quality recordings, CC-NC. 107 speakers with emotional variants for select speakers.

### CML-TTS (`cml-tts/fr/`)
French voices, CC BY 4.0. Enhanced versions available.

### Unmute Production (`unmute-prod-website/`)
Mixed licensing - check individual files.

## Voice URL Formats

```python
# Shorthand (pre-made voices)
"alba"

# HuggingFace protocol
"hf://kyutai/tts-voices/alba-mackenna/casual.wav"

# Full HuggingFace URL
"https://huggingface.co/kyutai/tts-voices/resolve/main/alba-mackenna/casual.wav"

# Local file
"./my_voice.wav"
"/absolute/path/to/voice.wav"
```

## Voice Cloning Tips

1. Use clean audio samples (minimal background noise)
2. 10+ seconds recommended for best results
3. Use [Adobe Podcast Enhance](https://podcast.adobe.com/en/enhance) to clean samples
4. Enhanced versions (`*_enhanced.wav`) often produce better results
