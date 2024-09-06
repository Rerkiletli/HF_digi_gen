from pydub import AudioSegment
from pydub.generators import Sine

# RTTY parameters
RTTY_BAUD = 45
RTTY_MARK = 1275     # Mark frequency for RTTY
RTTY_SPACE = 1445    # Space frequency for RTTY
RTTY_SHIFT = RTTY_SPACE - RTTY_MARK
RTTY_BIT_DURATION = 1000 / RTTY_BAUD  # Duration of one bit in milliseconds

# Updated Baudot (RTTY) according to ITA2
BAUDOT_CODE = {
    "00000": ("Blank", "Blank"),
    "00001": ("T", "5"),
    "00010": ("CR", "CR"),
    "00011": ("O", "9"),
    "00100": ("Space", "Space"),
    "00101": ("H", ""),
    "00110": ("N", ","),
    "00111": ("M", "."),
    "01000": ("Line Feed", "Line Feed"),
    "01001": ("L", ")"),
    "01010": ("R", "4"),
    "01011": ("G", "&"),
    "01100": ("I", "8"),
    "01101": ("P", "0"),
    "01110": ("C", ":"),
    "01111": ("V", ";"),
    "10000": ("E", "3"),
    "10001": ("Z", '"'),
    "10010": ("D", "$"),
    "10011": ("B", "?"),
    "10100": ("S", "BEL"),
    "10101": ("Y", "6"),
    "10110": ("F", "!"),
    "10111": ("X", "/"),
    "11000": ("A", "-"),
    "11001": ("W", "2"),
    "11010": ("J", "'"),
    "11011": ("Figure Shift", ""),
    "11100": ("U", "7"),
    "11101": ("Q", "1"),
    "11110": ("K", "("),
    "11111": ("Letter Shift", "")
}

# Create reverse lookup dictionaries to separate letters and figures
LETTERS_TO_BAUDOT = {v[0]: k for k, v in BAUDOT_CODE.items() if v[0] != ""}
FIGURES_TO_BAUDOT = {v[1]: k for k, v in BAUDOT_CODE.items() if v[1] != ""}

def encrypt(message):
    encoded = "11111"  # Start in LTRS mode
    current_mode = "LTRS"
    for char in message.upper():
        if char in FIGURES_TO_BAUDOT and current_mode != "FIGS":
            encoded += "11011"  # FIGS shift
            current_mode = "FIGS"
        elif char in LETTERS_TO_BAUDOT and current_mode != "LTRS":
            encoded += "11111"  # LTRS shift
            current_mode = "LTRS"
        
        if current_mode == "LTRS":
            encoded += LETTERS_TO_BAUDOT.get(char, LETTERS_TO_BAUDOT["Space"])
        else:
            encoded += FIGURES_TO_BAUDOT.get(char, FIGURES_TO_BAUDOT["Space"])
    return encoded

def decrypt(encoded_message):
    decoded = ""
    current_mode = "LTRS"
    i = 0
    while i < len(encoded_message):
        code = encoded_message[i:i+5]
        if code == "11011":
            current_mode = "FIGS"
        elif code == "11111":
            current_mode = "LTRS"
        else:
            char = BAUDOT_CODE[code][0 if current_mode == "LTRS" else 1]
            if char not in ["Blank", "CR", "Line Feed", "Space"]:
                decoded += char
            elif char == "Space":
                decoded += " "
            elif char == "Line Feed":
                decoded += "\n"
        i += 5
    return decoded

def generate_tone(freq, duration):
    return Sine(freq).to_audio_segment(duration=duration)

def turn_into_audio(message):
    audio = AudioSegment.empty()
    encoded_message = encrypt(message)
    for bit in encoded_message:
        audio += generate_tone(RTTY_MARK if bit == '1' else RTTY_SPACE, RTTY_BIT_DURATION)
    return audio, audio.frame_rate