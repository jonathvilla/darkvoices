# from core.tts_service import generate_voice
# from core.exporter import export_audio

# if __name__ == "__main__":
#     texto = "La puerta se cerró sola... y alguien respiraba detrás de ti."
#     mp3_path = generate_voice(texto, "terror.mp3")
#     wav_path = export_audio(mp3_path, "wav")

#     print(f"✅ Audio generado: {mp3_path}")
#     print(f"✅ Audio convertido: {wav_path}")

# main.py
from core.tts_service import generate_voice, list_speakers, list_languages

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
    output_path = "output/voz_final.wav"
    generate_voice(text, output_path, speaker=speaker, language=language)

    print(f"\n✅ Audio generado con éxito en: {output_path}\n")

if __name__ == "__main__":
    main()