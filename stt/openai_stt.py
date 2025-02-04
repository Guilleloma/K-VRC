# vkrc/stt/openai_stt.py
import openai
import os

class OpenAIWhisperSTT:
    def __init__(self, api_key=None):
        """
        api_key: puedes inyectar la clave en el constructor
                 o usar la variable de entorno OPENAI_API_KEY
        """
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = api_key

    def transcribe(self, audio_file_path, language="es", temperature=0.0):
        """
        Transcribe el archivo de audio usando OpenAI Whisper.
        :param audio_file_path: Ruta del archivo (wav, mp3, m4a, etc.)
        :param language: Idioma ('es', 'en', etc.)
        :param temperature: Parámetro de decodificación.
        :return: Texto transcrito como string.
        """
        with open(audio_file_path, "rb") as audio_file:
            response = openai.Audio.create(
                file=audio_file,
                model="whisper-1",
                # Atributos opcionales:
                # response_format="text",  # si quieres que devuelva solo el texto
                temperature=temperature,
                language=language
            )
        
        # Si NO usas response_format="text", 'response' es un dict con {"text": "transcrito..."}
        # Usaremos la clave "text":
        return response["text"]
