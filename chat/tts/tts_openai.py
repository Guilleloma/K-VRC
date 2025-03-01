# tts/tts_openai.py
from openai import OpenAI
import os
from pydub import AudioSegment
from pydub.playback import play
from dotenv import load_dotenv

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
            # Intenta usar el valor por defecto (que debería estar en la variable de entorno)
            self.client = OpenAI()  

    def texto_a_voz_streaming(self, texto, output_file="output.mp3", voice="fable", model="tts-1"):
        """
        Envía 'texto' a la API TTS de OpenAI, guarda la respuesta en 'output_file'
        y luego reproduce el archivo usando pydub.

        Si 'output_file' es una ruta relativa, se guardará en la carpeta 'tts' junto a este archivo.
        """
        # Si el output_file no es una ruta absoluta, construirla en la carpeta del módulo
        if not os.path.isabs(output_file):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            output_file = os.path.join(base_dir, output_file)
            output_file = os.path.abspath(output_file)
        
        print(f"[OpenAITTS] Iniciando TTS con streaming real-time...\nGuardando audio en: '{output_file}'")
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

if __name__ == "__main__":
    # Prueba de generación TTS; aquí se guardará 'output.mp3' en la carpeta 'tts'
    OpenAITTS().texto_a_voz_streaming("Hola, este es un ejemplo de TTS")
