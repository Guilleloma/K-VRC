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

    def generar_audio(self, texto, output_file="output.mp3", voice="nova", model="tts-1"):
        """
        Convierte texto a voz usando la API de OpenAI y guarda el resultado en un archivo,
        pero NO reproduce el audio (esto permite sincronizar la animación después).
        
        Args:
            texto (str): El texto a convertir a voz.
            output_file (str): Nombre del archivo de salida.
            voice (str): La voz a utilizar. Opciones: 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'.
            model (str): El modelo a utilizar. Opciones: 'tts-1', 'tts-1-hd'.
            
        Returns:
            str: Ruta al archivo de audio generado, o None si hubo un error.
        """
        try:
            print(f"[TTS] Generando audio para texto de {len(texto)} caracteres, usando voz: {voice}")
            
            # Generar el audio con la API de OpenAI
            response = self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=texto
            )
            
            # Guardar el audio en un archivo
            response.stream_to_file(output_file)
            
            # Devolver el nombre del archivo generado
            return output_file
            
        except Exception as e:
            print(f"[OpenAITTS] Error al generar audio: {e}")
            return None

    def texto_a_voz_streaming(self, texto, output_file="output.mp3", voice="nova", model="tts-1"):
        """
        Convierte texto a voz usando la API de OpenAI y guarda el resultado en un archivo.
        Luego reproduce el archivo usando el método reproducir_audio.
        
        Args:
            texto (str): El texto a convertir a voz.
            output_file (str): Nombre del archivo de salida.
            voice (str): La voz a utilizar. Opciones: 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'.
            model (str): El modelo a utilizar. Opciones: 'tts-1', 'tts-1-hd'.
        """
        try:
            audio_file = self.generar_audio(texto, output_file, voice, model)
            if audio_file:
                # Reproducir el audio
                self.reproducir_audio(audio_file)
            
        except Exception as e:
            print(f"[OpenAITTS] Error al generar o reproducir audio: {e}")

    def reproducir_audio(self, audio_file):
        """
        Reproduce un archivo MP3 usando únicamente mpg123, sin intentar usar pydub/PyAudio.
        """
        try:
            # Usamos directamente mpg123 para reproducir el MP3 en modo silencioso
            import subprocess
            print("[TTS] Reproduciendo audio...")
            subprocess.run(["mpg123", "-q", audio_file], check=False)
            print("[TTS] Reproducción finalizada.")
        except Exception as e:
            print(f"[TTS] Error: {e}")