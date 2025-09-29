from TTS.api import TTS

class TTSEngine:
    def __init__(self, model_name="tts_models/es/css10/vits", device="cpu"):
        self.tts = TTS(model_name).to(device)

    def synthesize(self, text, output_file="output/voice.wav"):
        self.tts.tts_to_file(
            text=text,
            file_path=output_file
        )
        return output_file