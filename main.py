import morse
import rtty
import navtex
import psk31
import mfsk16
import wav_to_iq

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
    
    # Handling potential differences in audio_func return values
    audio_result = audio_func(encrypted)
    if isinstance(audio_result, tuple):
        audio, sample_rate = audio_result
    else:
        audio = audio_result
        sample_rate = getattr(audio, 'frame_rate', 44100)  # Default to 44100 if not specified
    
    print(f"{mode.upper()} Encrypted: {encrypted}")
    print(f"{mode.upper()} Decrypted: {decrypted}")
    print(f"Sample rate: {sample_rate} Hz")
    
    wav_output = f"{save_path}/{mode}_message.wav"
    audio.export(wav_output, format="wav")
    print(f"{mode.upper()} audio saved as {wav_output}")

    iq_output = f"{save_path}/{mode}_message.iq"
    wav_to_iq.wav_to_iq(wav_output, iq_output)
    print(f"{mode.upper()} IQ data saved as {iq_output}")
    
    return encrypted, decrypted, wav_output, iq_output, sample_rate

if __name__ == "__main__":
    message = "THIS IS A TEST MESSAGE HELLO WORLD 12345"
    print("Original:", message)
    print("\n")
    
    modes = ['morse', 'rtty', 'navtex', 'psk31', 'mfsk16']
    
    for mode in modes:
        try:
            encrypted, decrypted, wav_file, iq_file, sample_rate = process_message(message, mode)
            print(f"Processed {mode.upper()}:")
            print(f"  Encrypted: {encrypted}")
            print(f"  Decrypted: {decrypted}")
            print(f"  WAV file: {wav_file}")
            print(f"  IQ file: {iq_file}")
            print(f"  Sample rate: {sample_rate} Hz")
            print()
        except Exception as e:
            print(f"Error processing {mode}: {str(e)}")
            print()
