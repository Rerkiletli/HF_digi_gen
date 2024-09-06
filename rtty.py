from pydub import AudioSegment
from pydub.generators import Sine

# RTTY parameters
RTTY_BAUD = 45
RTTY_MARK = 1275     # Mark frequency for RTTY
RTTY_SPACE = 1445    # Space frequency for RTTY
RTTY_SHIFT = RTTY_SPACE - RTTY_MARK
RTTY_BIT_DURATION = 1000 / RTTY_BAUD  # Duration of one bit in milliseconds

# Baudot code (RTTY)
BAUDOT_CODE = {
    'A': '11000', 'B': '10011', 'C': '01110', 'D': '10010', 'E': '10000', 'F': '10110', 'G': '01011', 'H': '00101',
    'I': '01100', 'J': '11010', 'K': '11110', 'L': '01001', 'M': '00111', 'N': '00110', 'O': '00011', 'P': '01101',
    'Q': '11101', 'R': '01010', 'S': '10100', 'T': '00001', 'U': '11100', 'V': '01111', 'W': '11001', 'X': '10111',
    'Y': '10101', 'Z': '10001', '0': '01010', '1': '10011', '2': '10111', '3': '00011', '4': '01011', '5': '10000',
    '6': '10101', '7': '11100', '8': '01100', '9': '11001', ' ': '00100', '\n': '01000', '\r': '00010',
    'FIGS': '11011', 'LTRS': '11111'
}

# RTTY functions
def encrypt(message):
    encoded = BAUDOT_CODE['LTRS']  # Start in LTRS mode
    current_mode = 'LTRS'
    for char in message.upper():
        if char.isdigit() or char in ['-', '?', ':', '(', ')', '.', '/']:
            if current_mode != 'FIGS':
                encoded += BAUDOT_CODE['FIGS']
                current_mode = 'FIGS'
        elif char.isalpha() or char == ' ':
            if current_mode != 'LTRS':
                encoded += BAUDOT_CODE['LTRS']
                current_mode = 'LTRS'
        encoded += BAUDOT_CODE.get(char, BAUDOT_CODE[' '])
    return encoded

def decrypt(encoded_message):
    reverse_baudot = {v: k for k, v in BAUDOT_CODE.items()}
    decoded = ''
    current_mode = 'LTRS'
    i = 0
    while i < len(encoded_message):
        code = encoded_message[i:i+5]
        char = reverse_baudot.get(code, ' ')
        if char == 'FIGS':
            current_mode = 'FIGS'
        elif char == 'LTRS':
            current_mode = 'LTRS'
        else:
            if current_mode == 'FIGS':
                if char.isalpha():
                    decoded += char.lower()
                else:
                    decoded += {'A': '-', 'B': '?', 'C': ':', 'D': '$', 'E': '3', 'F': '!', 'G': '&', 'H': '#', 'I': '8',
                                'J': '\'', 'K': '(', 'L': ')', 'M': '.', 'N': ',', 'O': '9', 'P': '0', 'Q': '1', 'R': '4',
                                'S': '\'', 'T': '5', 'U': '7', 'V': ';', 'W': '2', 'X': '/', 'Y': '6', 'Z': '+'}.get(char, char)
            else:
                decoded += char
        i += 5
    return decoded

def generate_tone(freq, duration):
    return Sine(freq).to_audio_segment(duration=duration)

def turn_into_audio(message):
    audio = AudioSegment.empty()
    for char in message.upper():
        # Start bit (space)
        audio += generate_tone(RTTY_SPACE, RTTY_BIT_DURATION)
        if char in BAUDOT_CODE:
            for bit in BAUDOT_CODE[char]:
                audio += generate_tone(RTTY_MARK if bit == '1' else RTTY_SPACE, RTTY_BIT_DURATION)
        # Stop bits (mark)
        audio += generate_tone(RTTY_MARK, RTTY_BIT_DURATION * 1.5)
    return audio, audio.frame_rate