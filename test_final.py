import simpleaudio as sa
from core.tts_service import generate_voice
from pydub import AudioSegment
import os

print("--- PRUEBA FINAL DE CADENA DE AUDIO ---")

# 1. Generar un archivo de audio de prueba
TEXTO_PRUEBA = "Si escuchas esto, la prueba final ha funcionado."
ARCHIVO_PRUEBA = "output/test_final_audio.wav"

print(f"1. Generando audio para la frase: '{TEXTO_PRUEBA}'")
try:
    generate_voice(TEXTO_PRUEBA, ARCHIVO_PRUEBA, language="es")
    print("   -> Audio generado con éxito.")
except Exception as e:
    print(f"   -> ERROR: No se pudo generar el audio TTS. Problema: {e}")
    exit()

# 2. Cargar el audio con Pydub
print(f"\n2. Cargando '{ARCHIVO_PRUEBA}' con pydub...")
try:
    audio_segment = AudioSegment.from_file(ARCHIVO_PRUEBA)
    print("   -> Audio cargado con éxito.")
except Exception as e:
    print(f"   -> ERROR: No se pudo cargar el audio con pydub. Problema: {e}")
    exit()

# 3. Intentar reproducir con SimpleAudio
print("\n3. Pasando los datos de pydub a simpleaudio para reproducir...")
try:
    play_obj = sa.play_buffer(
        audio_segment.raw_data,
        num_channels=audio_segment.channels,
        bytes_per_sample=audio_segment.sample_width,
        sample_rate=audio_segment.frame_rate
    )
    play_obj.wait_done()
    print("\n--- RESULTADO: ¡ÉXITO! ---")
    print("La cadena completa de audio funciona fuera de la GUI.")

except Exception as e:
    print("\n--- RESULTADO: ¡FALLO! ---")
    print("La reproducción con simpleaudio falló, incluso en un script aislado.")
    print(f"Detalle del error: {e}")

# Limpiar
os.remove(ARCHIVO_PRUEBA)
