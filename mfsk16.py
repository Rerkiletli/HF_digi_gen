from pydub import AudioSegment
from pydub.generators import Sine

# MFSK16 parameters
MFSK16_BAUD = 15.625
MFSK16_TONES = 16
MFSK16_BASE_FREQ = 1500
MFSK16_TONE_SPACING = 15.625

# MFSK16 functions
def encrypt(message):
    return ' '.join([str(ord(c)) for c in message.upper()])

def decrypt(encrypted_message):
    return ''.join([chr(int(c)) for c in encrypted_message.split()])

def generate_tone(freq, duration):
    return Sine(freq).to_audio_segment(duration=duration)

def turn_into_audio(message):
    audio = AudioSegment.empty()
    encrypted = encrypt(message)
    for char in encrypted:
        if char.isdigit():
            freq = MFSK16_BASE_FREQ + int(char) * MFSK16_TONE_SPACING
            audio += generate_tone(freq, 1000 / MFSK16_BAUD)
        elif char == ' ':
            audio += AudioSegment.silent(duration=1000 / MFSK16_BAUD)
    return audio, audio.frame_rate