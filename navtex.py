from pydub import AudioSegment
from pydub.generators import Sine

# NAVTEX and SITOR-B parameters
NAVTEX_BAUD = 100
NAVTEX_MARK = 1615   # Mark frequency for NAVTEX
NAVTEX_SPACE = 1785  # Space frequency for NAVTEX
NAVTEX_SHIFT = NAVTEX_SPACE - NAVTEX_MARK
NAVTEX_BIT_DURATION = 1000 / NAVTEX_BAUD

# CCIR 476-5 code for NAVTEX and SITOR-B
CCIR_476_CODE = {
    'A': '011000', 'B': '010011', 'C': '001110', 'D': '010010', 'E': '010000', 'F': '010110',
    'G': '011010', 'H': '001011', 'I': '001100', 'J': '011110', 'K': '011011', 'L': '001001',
    'M': '000111', 'N': '000110', 'O': '000011', 'P': '001101', 'Q': '011101', 'R': '001010',
    'S': '010100', 'T': '000001', 'U': '111000', 'V': '101110', 'W': '111010', 'X': '101011',
    'Y': '101101', 'Z': '101001', '-': '001111', '?': '000100', ':': '010111', '$': '110000',
    '!': '101010', '&': '001000', "'": '011100', '(': '001010', ')': '010010', '.': '010110',
    ',': '110011', '/': '110010', '+': '000010', '=': '110001', ' ': '100000',
    # Figure shift and Letter shift
    'FIGS': '011111', 'LTRS': '111111',
    # Digits (in figure shift mode)
    '0': '101010', '1': '011000', '2': '011001', '3': '010011', '4': '101101',
    '5': '000001', '6': '011010', '7': '001110', '8': '001100', '9': '011110'
}

def encrypt(message):
    encrypted = []
    shift_mode = 'LTRS'
    for char in message.upper():
        if char.isdigit() or char in ['?', ':', '-', '$', '!', '&', '(', ')', '.', ',', '/', '+', '=']:
            if shift_mode != 'FIGS':
                encrypted.append(CCIR_476_CODE['FIGS'])
                shift_mode = 'FIGS'
        elif char.isalpha() or char == ' ':
            if shift_mode != 'LTRS':
                encrypted.append(CCIR_476_CODE['LTRS'])
                shift_mode = 'LTRS'
        encrypted.append(CCIR_476_CODE.get(char, CCIR_476_CODE[' ']))
    return ''.join(encrypted)

def decrypt(encrypted_message):
    decrypted = []
    reverse_code = {v: k for k, v in CCIR_476_CODE.items()}
    shift_mode = 'LTRS'
    i = 0
    while i < len(encrypted_message):
        chunk = encrypted_message[i:i+6]
        if chunk == CCIR_476_CODE['FIGS']:
            shift_mode = 'FIGS'
        elif chunk == CCIR_476_CODE['LTRS']:
            shift_mode = 'LTRS'
        elif chunk in reverse_code:
            char = reverse_code[chunk]
            if shift_mode == 'FIGS' and char in '0123456789':
                decrypted.append(char)
            elif shift_mode == 'LTRS' and char.isalpha():
                decrypted.append(char)
            elif char in [' ', '-', '?', ':', '$', '!', '&', "'", '(', ')', '.', ',', '/', '+', '=']:
                decrypted.append(char)
        else:
            decrypted.append('?')
        i += 6
    return ''.join(decrypted)

def generate_tone(freq, duration):
    return Sine(freq).to_audio_segment(duration=duration)

def turn_into_audio(message):
    audio = AudioSegment.empty()
    # NAVTEX preamble
    for _ in range(10):
        audio += generate_tone(NAVTEX_MARK, NAVTEX_BIT_DURATION * 7)
        audio += generate_tone(NAVTEX_SPACE, NAVTEX_BIT_DURATION * 7)
    # Message
    encrypted = encrypt(message)
    for bit in encrypted:
        audio += generate_tone(NAVTEX_MARK if bit == '0' else NAVTEX_SPACE, NAVTEX_BIT_DURATION)
    # End of message
    audio += generate_tone(NAVTEX_MARK, NAVTEX_BIT_DURATION * 4)
    return audio, audio.frame_rate