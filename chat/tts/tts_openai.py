# tts/tts_openai.py
from openai import OpenAI
import os
from pydub import AudioSegment
from pydub.playback import play
from dotenv import load_dotenv
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
        En Raspberry Pi, primero convierte el audio a un formato compatible.
        """
        try:
            # Intentamos cargar el audio
            sound = AudioSegment.from_file(audio_file, format="mp3")
            
            # Verificamos si estamos en Raspberry Pi
            import sys
            sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
            from utils import is_raspberry_pi
            
            if is_raspberry_pi():
                # En Raspberry Pi, convertimos el audio a WAV de 44.1kHz (frecuencia estándar soportada)
                print("[OpenAITTS] Detectada Raspberry Pi, convirtiendo audio a formato compatible...")
                
                # Convertir a una frecuencia de muestreo estándar (44.1kHz)
                sound = sound.set_frame_rate(44100)
                
                # Crear un archivo temporal para el WAV convertido
                temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
                wav_path = temp_wav.name
                temp_wav.close()
                
                # Exportar a WAV
                sound.export(wav_path, format="wav")
                
                # Reproducir usando un comando del sistema en lugar de PyDub
                import subprocess
                print(f"[OpenAITTS] Reproduciendo audio convertido con aplay...")
                result = subprocess.run(["aplay", wav_path], capture_output=True)
                
                # Eliminar el archivo temporal
                os.unlink(wav_path)
                
                if result.returncode != 0:
                    print(f"[OpenAITTS] Error al reproducir con aplay: {result.stderr.decode()}")
                    # Como fallback, intentamos reproducir con mpg123
                    print("[OpenAITTS] Intentando reproducir con mpg123...")
                    subprocess.run(["mpg123", audio_file], capture_output=True)
            else:
                # En otros sistemas usamos pydub normalmente
                play(sound)
                
            print("[OpenAITTS] Reproducción de audio finalizada.")
            
        except Exception as e:
            print(f"[OpenAITTS] Error al reproducir '{audio_file}': {e}")
            
            # Si falla la reproducción, intentamos usar mpg123 como último recurso
            try:
                import subprocess
                print("[OpenAITTS] Intentando reproducir con mpg123 como último recurso...")
                subprocess.run(["mpg123", audio_file], capture_output=True)
            except Exception as fallback_error:
                print(f"[OpenAITTS] Falló también el fallback mpg123: {fallback_error}")

if __name__ == "__main__":
    # Prueba de generación TTS; aquí se guardará 'output.mp3' en la carpeta 'tts'
    OpenAITTS().texto_a_voz_streaming("Hola, este es un ejemplo de TTS")
