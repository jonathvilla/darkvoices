# audio_processor.py
from pydub import AudioSegment

class AudioProcessor:
    def __init__(self, voice_file):
        self.voice = AudioSegment.from_file(voice_file)

    def add_background(self, bg_file, output_file="output/final.wav"):
        background = AudioSegment.from_file(bg_file)
        final = self.voice.overlay(background - 15)  # -15 = baja volumen ambiente
        final.export(output_file, format="wav")
        return output_file

    def add_echo(self, output_file="output/echo.wav"):
        # Simulación simple de eco duplicando la pista
        echo = self.voice + AudioSegment.silent(duration=200)
        final = self.voice.overlay(echo - 10)
        final.export(output_file, format="wav")
        return output_file
