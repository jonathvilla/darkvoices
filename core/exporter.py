from pydub import AudioSegment
import os

def export_audio(input_path: str, format: str = "wav") -> str:
    """
    Convierte un archivo MP3 a otro formato (wav, ogg, flac).
    Retorna la ruta del archivo exportado.
    """
    sound = AudioSegment.from_file(input_path)
    output_path = os.path.splitext(input_path)[0] + f".{format}"
    sound.export(output_path, format=format)
    return output_path