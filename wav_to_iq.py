import numpy as np
from scipy.io import wavfile
from scipy.signal import hilbert
import struct

def wav_to_iq(input_wav, output_iq):
    # Read the WAV file
    sample_rate, data = wavfile.read(input_wav)
    
    # If stereo, convert to mono by taking the mean of both channels
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)
    
    # Normalize the data
    data = data.astype(float) / np.max(np.abs(data))
    
    # Generate analytic signal using Hilbert transform
    analytic_signal = hilbert(data)
    
    # Extract I and Q components
    i_data = np.real(analytic_signal)
    q_data = np.imag(analytic_signal)
    
    # Interleave I and Q samples
    iq_data = np.empty((len(i_data) * 2,), dtype=np.float32)
    iq_data[0::2] = i_data
    iq_data[1::2] = q_data
    
    # Save IQ data with a simple header containing the sample rate
    with open(output_iq, 'wb') as f:
        f.write(struct.pack('I', sample_rate))  # Write sample rate as 4-byte integer
        iq_data.tofile(f)
    
    print(f"IQ data saved to {output_iq}")
    return sample_rate