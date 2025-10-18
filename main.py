# main.py
from core.tts_service import generate_voice, list_speakers, list_languages
from core.audio_processor import AudioProcessor
import re

def main():
    print("🎙️ Bienvenido a DarkVoices - Generador de voces de terror y suspenso 🎧")
    
    # 1️⃣ Texto a narrar
    text = input("\n👉 Escribe el texto que quieres convertir en audio:\n> ")

    # 2️⃣ Elegir idioma
    languages = list_languages()
    language = None
    if languages:
        print("\n🌍 Idiomas disponibles:", languages)
        lang_input = input("👉 Escribe el código del idioma (ej: es, en, pt) [default=es]: ") or "es"
        if lang_input in languages:
            language = lang_input
        else:
            print("⚠️ Idioma no válido, usando español (es).")
            language = "es"

    # 3️⃣ Elegir voz (solo si hay varias)
    speakers = list_speakers(language)
    speaker = None
    if speakers and speakers != ["default"]:
        print("\n🎭 Voces disponibles:")
        for i, spk in enumerate(speakers):
            print(f"{i+1}. {spk.strip()}")
        try:
            choice = int(input("\n👉 Elige el número de la voz (default=1): ") or 1)
            speaker = speakers[choice-1].strip()
        except (ValueError, IndexError):
            print("⚠️ Elección inválida, usando la primera voz.")
            speaker = speakers[0].strip()

    # 4️⃣ Generar archivo
    # Crear un nombre de archivo dinámico a partir del texto
    safe_filename = "_".join(re.sub(r'[^\w_]', '', word) for word in text.split()[:3]).lower()
    output_path = f"output/{safe_filename}.wav"
    
    generate_voice(text, output_path, speaker=speaker, language=language)

    print(f"\n✅ Audio generado con éxito en: {output_path}")

    # 5️⃣ (Opcional) Añadir efectos de audio
    # choice = input("\n👉 ¿Quieres añadir música de fondo? (s/n) [default=n]: ") or "n"
    # if choice.lower() == 's':
    #     # Deberás tener un archivo de audio en data/sounds/
    #     # Por ejemplo: data/sounds/terror_background.mp3
    #     processor = AudioProcessor(output_path)
    #     final_audio = processor.add_background("data/sounds/terror_background.mp3", f"output/{safe_filename}_con_fondo.wav")
    #     print(f"\n✅ Audio con fondo generado en: {final_audio}\n")


if __name__ == "__main__":
    main()