# tts_openai.py
from openai import OpenAI
import os
from pydub import AudioSegment
from pydub.playback import play

class OpenAITTS:
    """
    Clase que encapsula la llamada a la API de TTS de OpenAI 
    (la que supuestamente existe como 'client.audio.speech.create').
    """
    def __init__(self, api_key=None):
        """
        Inicializa el cliente con la API key de OpenAI.
        Si no se pasa clave, se puede leer de variable de entorno en tu SDK modificado.
        """
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            # Si tu SDK modificado ya soporta leer la key de la variable de entorno,
            # podrías usar directamente `self.client = OpenAI()`
            self.client = OpenAI()  

    def texto_a_voz_streaming(self, texto, output_file="output.mp3", voice="alloy", model="tts-1"):
        """
        Envía 'texto' a la API TTS de OpenAI, guarda la respuesta en 'output_file'
        y luego reproduce el archivo usando pydub.
        """
        print("[OpenAITTS] Iniciando TTS con streaming real-time...")
        try:
            response = self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=texto
            )
            # Guarda el audio en un archivo local al vuelo
            response.stream_to_file(output_file)

            print(f"[OpenAITTS] Audio guardado en '{output_file}'. Reproduciendo...")
            self.reproducir_audio(output_file)

        except Exception as e:
            print(f"[OpenAITTS] Error en la solicitud TTS: {e}")

    def reproducir_audio(self, audio_file):
        """
        Reproduce un archivo MP3 (o ajusta si es WAV, etc.).
        """
        try:
            sound = AudioSegment.from_file(audio_file, format="mp3")
            play(sound)
            print("[OpenAITTS] Reproducción de audio finalizada.")
        except Exception as e:
            print(f"[OpenAITTS] Error al reproducir '{audio_file}': {e}")
