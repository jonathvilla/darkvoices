from pydub import AudioSegment
from pydub.effects import speedup

class AudioProcessor:
    def __init__(self, audio_segment: AudioSegment):
        self.voice = audio_segment

    @classmethod
    def from_file(cls, file_path):
        audio_segment = AudioSegment.from_file(file_path)
        return cls(audio_segment)

    def adjust_pitch(self, semitones):
        """ Ajusta el tono de la voz. `semitones` puede ser positivo (más agudo) o negativo (más grave). """
        if semitones == 0:
            return self
        
        new_rate = int(self.voice.frame_rate * (2.0 ** (semitones / 12.0)))
        self.voice = self.voice._spawn(self.voice.raw_data, overrides={'frame_rate': new_rate})
        return self

    def adjust_speed(self, speed):
        """ Ajusta la velocidad. `speed` > 1.0 para más rápido, < 1.0 para más lento. """
        if speed == 1.0:
            return self
        
        self.voice = speedup(self.voice, playback_speed=speed)
        return self

    def add_echo(self, delay_ms=200, decay=0.4):
        """ Añade un efecto de eco. `decay` es el factor de atenuación del eco. """
        if delay_ms == 0:
            return self
            
        echo = self.voice + AudioSegment.silent(duration=delay_ms)
        # El volumen del eco se reduce por el factor de decaimiento
        self.voice = self.voice.overlay(echo - (1 - decay) * 100)
        return self

    def add_background(self, bg_file, volume_db=-15):
        """ Añade un sonido de fondo. """
        background = AudioSegment.from_file(bg_file)
        self.voice = self.voice.overlay(background + volume_db)
        return self

    def save(self, output_file, format="wav"):
        """ Guarda el audio procesado en un archivo. """
        self.voice.export(output_file, format=format)
        return output_file
