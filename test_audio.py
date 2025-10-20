import simpleaudio as sa
import numpy as np

# Generar un tono de prueba (La a 440 Hz)
frequency = 440  # Hz
fs = 44100  # Tasa de muestreo
seconds = 2  # Duración
t = np.linspace(0, seconds, seconds * fs, False)
note = np.sin(frequency * t * 2 * np.pi)
audio = note * (2**15 - 1) / np.max(np.abs(note))
audio = audio.astype(np.int16)

print("Intentando reproducir un tono de 2 segundos con simpleaudio...")
try:
    play_obj = sa.play_buffer(audio, 1, 2, fs)
    play_obj.wait_done()
    print("¡Prueba finalizada!")
except Exception as e:
    print("\n--- ERROR ---")
    print("simpleaudio no pudo reproducir el sonido.")
    print(f"Detalle del error: {e}")
