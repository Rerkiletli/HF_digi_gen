from pydub import AudioSegment
from pydub.generators import Sine

# Morse code parameters
DOT_DURATION = 100   # Duration of a dot in milliseconds
DASH_DURATION = 300  # Duration of a dash in milliseconds
MORSE_FREQUENCY = 800  # Frequency of the tone in Hz
MORSE_DELAY = 25     # Delay between Morse code elements in milliseconds
MORSE_SPACE = 100    # Space between words in milliseconds
SAMPLE_RATE = 44100  # Sample rate for audio generation

# Morse code dictionary
MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', ', ': '--..--',
    '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-'
}

# Encrypt message into Morse code
def encrypt(message):
    return ' '.join(MORSE_CODE.get(char.upper(), '') if char.upper() in MORSE_CODE else '|' for char in message)

# Decrypt Morse code message
def decrypt(message):
    reverse_morse = {v: k for k, v in MORSE_CODE.items()}
    return ''.join(reverse_morse.get(code, '') if code != '|' else ' ' for code in message.split())

# Generate Morse code audio
def generate_morse_audio(morse_code):
    audio = AudioSegment.silent(duration=0)
    
    for symbol in morse_code:
        if symbol == '.':
            tone = Sine(MORSE_FREQUENCY).to_audio_segment(duration=DOT_DURATION, sample_rate=SAMPLE_RATE)
        elif symbol == '-':
            tone = Sine(MORSE_FREQUENCY).to_audio_segment(duration=DASH_DURATION, sample_rate=SAMPLE_RATE)
        elif symbol == ' ':
            tone = AudioSegment.silent(duration=MORSE_DELAY)
        elif symbol == '|':
            tone = AudioSegment.silent(duration=MORSE_SPACE)
        else:
            continue
        
        audio += tone
        audio += AudioSegment.silent(duration=MORSE_DELAY)
    
    return audio

def generate_tone(freq, duration):
    return Sine(freq).to_audio_segment(duration=duration)

def turn_into_audio(message):
    audio = AudioSegment.empty()
    for char in message:
        if char == '.':
            audio += generate_tone(MORSE_FREQUENCY, DOT_DURATION)
        elif char == '-':
            audio += generate_tone(MORSE_FREQUENCY, DASH_DURATION)
        elif char == ' ':
            audio += AudioSegment.silent(duration=MORSE_SPACE)
        audio += AudioSegment.silent(duration=MORSE_DELAY)
    return audio, audio.frame_rate