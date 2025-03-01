# tts/tts_openai.py
from openai import OpenAI
import os
from pydub import AudioSegment
from pydub.playback import play
from dotenv import load_dotenv
from utils import is_raspberry_pi
import tempfile

# Cargar variables de entorno desde .env
load_dotenv()

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
        elif os.getenv("OPENAI_API_KEY"):
            # Usar la clave leída del archivo .env
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        else:
            # Intenta usar el valor por defecto
            self.client = OpenAI()  

    # [el resto del código]

    def reproducir_audio(self, audio_file):
        """
        Reproduce un archivo MP3 usando únicamente mpg123, sin intentar usar pydub/PyAudio.
        """
        try:
            # Usamos directamente mpg123 para reproducir el MP3 - sin conversiones ni alternativas
            import subprocess
            print("[OpenAITTS] Reproduciendo directamente con mpg123...")
            subprocess.run(["mpg123", audio_file], check=False)
            print("[OpenAITTS] Reproducción finalizada.")
        except Exception as e:
            print(f"[OpenAITTS] Error: {e}")