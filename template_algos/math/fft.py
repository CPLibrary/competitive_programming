import numpy as np

def multiply_polynomials(a, b):
    """Multiply two polynomials using FFT."""
    n = len(a) + len(b) - 1
    size = 1 << (n-1).bit_length()
    fa = np.fft.fft(a, size)
    fb = np.fft.fft(b, size)
    fc = fa * fb
    c = np.fft.ifft(fc).real.round().astype(int)
    return c[:n]
