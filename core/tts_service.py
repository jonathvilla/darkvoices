# from gtts import gTTS
# from config.settings import LANGUAGE, OUTPUT_DIR
# import os

# def generate_voice(text: str, filename: str = "terror.mp3") -> str:
#     """
#     Genera un archivo de audio a partir de texto.
#     Retorna la ruta del archivo generado.
#     """
#     path = os.path.join(OUTPUT_DIR, filename)
#     tts = gTTS(text=text, lang=LANGUAGE)
#     tts.save(path)
#     return path
# 🔧 Modelo que quieres usar (puedes cambiarlo en config/settings.py)
from TTS.api import TTS

# Diccionario de modelos por idioma
MODELS = {
    "es": "tts_models/es/css10/vits",                 # Español
    "en": "tts_models/en/ljspeech/tacotron2-DDC",     # Inglés
    "pt": "tts_models/pt/cv/vits"                     # Portugués (extra)
}

# Cacheamos modelos cargados para evitar recargas
loaded_models = {}

def get_tts(language="es"):
    if language not in MODELS:
        raise ValueError(f"Idioma {language} no soportado. Usa {list(MODELS.keys())}")

    if language not in loaded_models:
        print(f"[INFO] Cargando modelo para {language}...")
        loaded_models[language] = TTS(MODELS[language]).to("cpu")

    return loaded_models[language]

def list_languages():
    """Lista los idiomas soportados por DarkVoices."""
    return list(MODELS.keys())

def list_speakers(language="es"):
    """Lista las voces disponibles para un idioma específico."""
    tts = get_tts(language)
    if hasattr(tts, "speakers") and tts.speakers:
        return list(tts.speakers)
    return ["default"]  # fallback si solo hay una voz

def generate_voice(text, output_path, speaker=None, language="es"):
    """Genera el audio según el idioma y voz seleccionados."""
    tts = get_tts(language)

    args = {"text": text, "file_path": output_path}

    # Solo pasar speaker si el modelo es multi-speaker
    if hasattr(tts, "speakers") and tts.speakers:
        if speaker:
            args["speaker"] = speaker

    tts.tts_to_file(**args)
    return output_path