import customtkinter as ctk
from core.tts_service import generate_voice, list_languages, list_speakers
from core.audio_processor import AudioProcessor
from pydub import AudioSegment
import simpleaudio as sa
import re
import threading
import os

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.is_playing = False
        self.preview_file_path = os.path.join("output", "preview_cache.wav")

        self.title("DarkVoices - Generador de Audio")
        self.geometry("700x750")

        # --- Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Widgets ---
        self.textbox = ctk.CTkTextbox(self, wrap="word")
        self.textbox.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="nsew")

        # --- Options Frame ---
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        self.options_frame.grid_columnconfigure(1, weight=1)

        # Language & Speaker
        self.language_label = ctk.CTkLabel(self.options_frame, text="Idioma:")
        self.language_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.languages = list_languages()
        self.language_var = ctk.StringVar(value=self.languages[0] if self.languages else "")
        self.language_menu = ctk.CTkOptionMenu(self.options_frame, variable=self.language_var, values=self.languages, command=self.update_speakers)
        self.language_menu.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.speaker_label = ctk.CTkLabel(self.options_frame, text="Voz:")
        self.speaker_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.speaker_var = ctk.StringVar(value="")
        self.speaker_menu = ctk.CTkOptionMenu(self.options_frame, variable=self.speaker_var, values=[])
        self.speaker_menu.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # --- Equalizer Frame ---
        self.equalizer_frame = ctk.CTkFrame(self, fg_color="#2B2B2B")
        self.equalizer_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        self.equalizer_frame.grid_columnconfigure(1, weight=1)

        self.pitch_label = ctk.CTkLabel(self.equalizer_frame, text="Tono (Pitch):")
        self.pitch_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.pitch_slider = ctk.CTkSlider(self.equalizer_frame, from_=-12, to=12, number_of_steps=24, command=lambda v: self.pitch_value.configure(text=f"{v:.1f}"))
        self.pitch_slider.set(0)
        self.pitch_slider.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.pitch_value = ctk.CTkLabel(self.equalizer_frame, text="0.0")
        self.pitch_value.grid(row=0, column=2, padx=10, pady=10)

        self.speed_label = ctk.CTkLabel(self.equalizer_frame, text="Velocidad (Desactivado):")
        self.speed_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.speed_slider = ctk.CTkSlider(self.equalizer_frame, from_=0.5, to=2.0, number_of_steps=15, command=lambda v: self.speed_value.configure(text=f"{v:.2f}"))
        self.speed_slider.set(1.0)
        self.speed_slider.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.speed_value = ctk.CTkLabel(self.equalizer_frame, text="1.00")
        self.speed_value.grid(row=1, column=2, padx=10, pady=10)

        # --- Action Buttons Frame ---
        self.action_frame = ctk.CTkFrame(self)
        self.action_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.action_frame.grid_columnconfigure(1, weight=1)

        self.generate_button = ctk.CTkButton(self.action_frame, text="Generar y Guardar", command=self.start_save_thread)
        self.generate_button.grid(row=0, column=0, padx=(0, 5), pady=0, sticky="ew")

        self.preview_button = ctk.CTkButton(self.action_frame, text="Previsualizar", command=self.start_preview_thread)
        self.preview_button.grid(row=0, column=1, padx=(5, 0), pady=0, sticky="ew")
        
        self.status_label = ctk.CTkLabel(self, text="Listo.")
        self.status_label.grid(row=4, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")

        self.update_speakers(self.language_var.get())

    def update_speakers(self, selected_language):
        speakers = list_speakers(selected_language)
        self.speaker_menu.configure(values=speakers)
        if speakers:
            self.speaker_var.set(speakers[0])
        else:
            self.speaker_var.set("")

    def set_ui_state(self, state):
        self.generate_button.configure(state=state)
        self.preview_button.configure(state=state)

    def start_save_thread(self):
        threading.Thread(target=self.save_task, daemon=True).start()

    def start_preview_thread(self):
        threading.Thread(target=self.preview_task, daemon=True).start()

    def _play_audio_file(self, file_path):
        if self.is_playing:
            return
        try:
            self.is_playing = True
            self.after(0, lambda: self.status_label.configure(text="Reproduciendo..."))
            
            audio_segment = AudioSegment.from_file(file_path)
            play_obj = sa.play_buffer(
                audio_segment.raw_data,
                num_channels=audio_segment.channels,
                bytes_per_sample=audio_segment.sample_width,
                sample_rate=audio_segment.frame_rate
            )
            play_obj.wait_done()
        finally:
            self.is_playing = False
            self.after(0, lambda: self.status_label.configure(text="Listo."))

    def _generate_processed_audio(self):
        """Generates, processes, and saves audio to the preview cache file. Returns the path."""
        text = self.textbox.get("1.0", "end-1c")
        if not text.strip():
            self.after(0, lambda: self.status_label.configure(text="Error: El campo de texto está vacío."))
            return None

        self.after(0, lambda: self.status_label.configure(text="Generando audio base..."))
        base_output_path = os.path.join("output", "base_temp.wav")
        generate_voice(text, base_output_path, speaker=self.speaker_var.get(), language=self.language_var.get())

        self.after(0, lambda: self.status_label.configure(text="Aplicando efectos..."))
        pitch = self.pitch_slider.get()
        # speed = self.speed_slider.get() # TEMPORARILY DISABLED
        audio_processor = AudioProcessor.from_file(base_output_path)
        audio_processor.adjust_pitch(pitch)
        # audio_processor.adjust_speed(speed) # TEMPORARILY DISABLED
        
        audio_processor.save(self.preview_file_path)
        os.remove(base_output_path)
        return self.preview_file_path

    def preview_task(self):
        self.after(0, lambda: self.set_ui_state("disabled"))
        try:
            processed_file = self._generate_processed_audio()
            if processed_file:
                self._play_audio_file(processed_file)
        except Exception as e:
            self.after(0, lambda e=e: self.status_label.configure(text=f"Error: {e}"))
        finally:
            self.after(0, lambda: self.set_ui_state("normal"))

    def save_task(self):
        self.after(0, lambda: self.set_ui_state("disabled"))
        try:
            processed_file = self._generate_processed_audio()
            if processed_file:
                safe_filename = "_".join(re.sub(r'[^\w_]', '', word) for word in self.textbox.get("1.0", "end-1c").split()[:3]).lower() or "audio"
                final_output_path = os.path.join("output", f"{safe_filename}_guardado.wav")
                os.rename(processed_file, final_output_path)
                self.after(0, lambda: self.status_label.configure(text=f"¡Audio guardado en {final_output_path}!"))
        except Exception as e:
            self.after(0, lambda e=e: self.status_label.configure(text=f"Error: {e}"))
        finally:
            self.after(0, lambda: self.set_ui_state("normal"))

if __name__ == "__main__":
    app = App()
    app.mainloop()
