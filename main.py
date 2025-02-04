import morse
import rtty
import navtex
import psk31
import mfsk16
import wav_to_iq
import os

save_path = "outputs"

def process_message(message, mode):
    modes = {
        'morse': (morse.encrypt, morse.decrypt, morse.turn_into_audio),
        'rtty': (rtty.encrypt, rtty.decrypt, rtty.turn_into_audio),
        'navtex': (navtex.encrypt, navtex.decrypt, navtex.turn_into_audio),
        'psk31': (psk31.encrypt, psk31.decrypt, psk31.turn_into_audio),
        'mfsk16': (mfsk16.encrypt, mfsk16.decrypt, mfsk16.turn_into_audio)
    }
    if mode not in modes:
        raise ValueError(f"Unsupported mode: {mode}")
    
    encrypt, decrypt, audio_func = modes[mode]
    
    encrypted = encrypt(message)
    decrypted = decrypt(encrypted)

    audio, sample_rate = audio_func(encrypted)
    
    print(f"\n{mode.upper()} Encrypted: {encrypted}")
    print(f"{mode.upper()} Decrypted: {decrypted}")
    print(f"Sample rate: {sample_rate} Hz")

    os.makedirs(save_path, exist_ok=True)
    wav_output = f"{save_path}/{mode}_message.wav"
    audio.export(wav_output, format="wav")
    print(f"{mode.upper()} audio saved as {wav_output}")

    iq_output = f"{save_path}/{mode}_message.iq"
    wav_to_iq.wav_to_iq(wav_output, iq_output)
    print(f"IQ data saved to {iq_output}")
    
    return encrypted, decrypted, wav_output, iq_output, sample_rate

if __name__ == "__main__":
    message = input("Enter your message: ")
    
    print("Select a mode to process the message:")
    print("1. Morse code")
    print("2. RTTY")
    print("3. NAVTEX")
    print("4. PSK31")
    print("5. MFSK16")
    print("6. All modes")
    mode_choice = input("Enter the mode number: ")

    mode_map = {
        "1": ['morse'],
        "2": ['rtty'],
        "3": ['navtex'],
        "4": ['psk31'],
        "5": ['mfsk16'],
        "6": ['morse', 'rtty', 'navtex', 'psk31', 'mfsk16']
    }

    modes = mode_map.get(mode_choice)
    if not modes:
        print("Invalid mode selection. Exiting.")
        exit()
    
    for mode in modes:
        try:
            encrypted, decrypted, wav_file, iq_file, sample_rate = process_message(message, mode)
        except Exception as e:
            print(f"Error processing {mode}: {str(e)}")
            print()