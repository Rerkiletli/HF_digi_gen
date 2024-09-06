
# Message Processing Script

This script processes messages using various encoding modes, converts the resulting audio to WAV format, and then generates IQ data from the WAV files. It supports the following modes:

- Morse Code (`morse`)
- RTTY (Radio Teletype) (`rtty`)
- NAVTEX (`navtex`)
- PSK31 (`psk31`)
- MFSK16 (`mfsk16`)

## Features

- **Encryption and Decryption:** The script encrypts and decrypts messages based on the selected mode.
- **Audio Generation:** Converts encrypted messages into audio files.
- **WAV and IQ File Creation:** Saves the audio files as WAV format and converts them into IQ data.

## Requirements

Make sure you have the following dependencies installed:

- `morse` (a module for Morse code)
- `rtty` (a module for RTTY encoding)
- `navtex` (a module for NAVTEX encoding)
- `psk31` (a module for PSK31 encoding)
- `mfsk16` (a module for MFSK16 encoding)
- `wav_to_iq` (a module to convert WAV files to IQ format)
- `pydub` (for audio file manipulation)

You can install `pydub` using pip if it's not already installed:

```bash
pip install pydub
```
