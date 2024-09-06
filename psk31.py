from pydub import AudioSegment
from pydub.generators import Sine
import numpy as np

# PSK31 parameters
PSK31_BAUD = 31.25
PSK31_FREQ = 1000  # Center frequency
PSK31_SAMPLE_RATE = 44100
PSK31_SAMPLES_PER_SYMBOL = int(PSK31_SAMPLE_RATE / PSK31_BAUD)

# Varicode for PSK31
VARICODE = {
    'A': '1011000', 'B': '1011100', 'C': '1011110', 'D': '1011111', 'E': '110',
    'F': '1101100', 'G': '1101110', 'H': '1101111', 'I': '1110', 'J': '1110100',
    'K': '1110110', 'L': '1110111', 'M': '1111000', 'N': '1111010', 'O': '1111011',
    'P': '1111100', 'Q': '1111110', 'R': '1111111', 'S': '10100', 'T': '10110',
    'U': '10111100', 'V': '10111110', 'W': '10111111', 'X': '11100100', 'Y': '11100110',
    'Z': '11100111', '0': '10110100', '1': '10110110', '2': '10110111', '3': '10111000',
    '4': '10111010', '5': '10111011', '6': '11100000', '7': '11100010', '8': '11100011',
    '9': '11100111', ' ': '1', '\n': '11101'
}

# PSK31 functions
def psk31_modulate(bits):
    t = np.arange(0, len(bits) * PSK31_SAMPLES_PER_SYMBOL) / PSK31_SAMPLE_RATE
    base_signal = np.sin(2 * np.pi * PSK31_FREQ * t)
    modulated = np.zeros_like(base_signal)
    for i, bit in enumerate(bits):
        start = i * PSK31_SAMPLES_PER_SYMBOL
        end = (i + 1) * PSK31_SAMPLES_PER_SYMBOL
        modulated[start:end] = base_signal[start:end] if bit == '1' else -base_signal[start:end]
    return modulated

def encrypt(message):
    return ''.join(VARICODE.get(char.upper(), VARICODE[' ']) + '00' for char in message) + '00000000'

def decrypt(encoded_message):
    reverse_varicode = {v: k for k, v in VARICODE.items()}
    decoded = ''
    buffer = ''
    for bit in encoded_message:
        buffer += bit
        if buffer.endswith('00'):
            if buffer[:-2] in reverse_varicode:
                decoded += reverse_varicode[buffer[:-2]]
            buffer = ''
    return decoded


def generate_tone(freq, duration):
    return Sine(freq).to_audio_segment(duration=duration)

def turn_into_audio(message):
    bits = encrypt(message)
    modulated_signal = psk31_modulate(bits)
    audio = np.int16(modulated_signal * 32767)
    return AudioSegment(audio.tobytes(), frame_rate=PSK31_SAMPLE_RATE, sample_width=2, channels=1), PSK31_SAMPLE_RATE