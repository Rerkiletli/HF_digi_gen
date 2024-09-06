from pydub import AudioSegment
from pydub.generators import Sine

# NAVTEX and SITOR-B parameters
NAVTEX_BAUD = 100
NAVTEX_MARK = 1615   # Mark frequency for NAVTEX
NAVTEX_SPACE = 1785  # Space frequency for NAVTEX
NAVTEX_SHIFT = NAVTEX_SPACE - NAVTEX_MARK
NAVTEX_BIT_DURATION = 1000 / NAVTEX_BAUD

# CCIR 476 code for NAVTEX and SITOR-B
CCIR_476_CODE = {
    'A': '011000', 'B': '010011', 'C': '011110', 'D': '010010', 'E': '010000', 'F': '010110',
    'G': '011011', 'H': '001011', 'I': '001100', 'J': '011010', 'K': '011110', 'L': '001001',
    'M': '001110', 'N': '001101', 'O': '000011', 'P': '001101', 'Q': '011101', 'R': '001010',
    'S': '010100', 'T': '000001', 'U': '011100', 'V': '001111', 'W': '011001', 'X': '010111',
    'Y': '010101', 'Z': '010001', '0': '010110', '1': '010011', '2': '010111', '3': '000011',
    '4': '001011', '5': '010000', '6': '010101', '7': '011100', '8': '001100', '9': '011001',
    ' ': '100000', '\n': '000010', '\r': '001000', '-': '001111', '?': '000111', ':': '010110',
    '$': '010010', '!': '011110', '&': '011011', "'": '011000', '(': '011110', ')': '001001',
    '.': '001110', ',': '001101', ';': '001111', '/': '010111', '+': '010001'
}

# NAVTEX and SITOR-B functions
def encrypt(message):
    return ''.join(CCIR_476_CODE.get(char.upper(), CCIR_476_CODE[' ']) for char in message)

def decrypt(encoded_message):
    reverse_ccir = {v: k for k, v in CCIR_476_CODE.items()}
    return ''.join(reverse_ccir.get(encoded_message[i:i+6], ' ') for i in range(0, len(encoded_message), 6))


def generate_tone(freq, duration):
    return Sine(freq).to_audio_segment(duration=duration)

def turn_into_audio(message):
    audio = AudioSegment.empty()
    # NAVTEX preamble
    for _ in range(10):
        audio += generate_tone(NAVTEX_MARK, NAVTEX_BIT_DURATION * 7)
        audio += generate_tone(NAVTEX_SPACE, NAVTEX_BIT_DURATION * 7)
    # Message
    for char in message.upper():
        if char in CCIR_476_CODE:
            for bit in CCIR_476_CODE[char]:
                audio += generate_tone(NAVTEX_MARK if bit == '1' else NAVTEX_SPACE, NAVTEX_BIT_DURATION)
    # End of message
    audio += generate_tone(NAVTEX_MARK, NAVTEX_BIT_DURATION * 4)
    return audio, audio.frame_rate