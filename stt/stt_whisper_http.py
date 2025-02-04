# stt_whisper_http.py
import os
import requests

def transcribe_file(file_path, language="es", temperature=0.0):
    """
    Envía un archivo de audio al endpoint /v1/audio/transcriptions
    de OpenAI para transcribir con 'whisper-1'.
    Requiere openai>=1.0.0, pero la hacemos manual con 'requests'.
    """
    url = "https://api.openai.com/v1/audio/transcriptions"

    # Lee la API key desde la variable de entorno
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("La variable OPENAI_API_KEY no está configurada en el entorno.")

    # Preparamos el archivo de audio y los parámetros
    with open(file_path, "rb") as f:
        files = {
            "file": (file_path, f, "application/octet-stream")
        }
        data = {
            "model": "whisper-1",
            "language": language,
            "temperature": temperature,
            # "prompt": "Opcional",
            # "response_format": "text",  # si quieres que devuelva sólo texto en vez de JSON
        }
        headers = {
            "Authorization": f"Bearer {api_key}"
        }

        # Llamada POST al endpoint de transcripciones
        response = requests.post(url, headers=headers, data=data, files=files)
    
    # Si la respuesta no es 2xx, lanza excepción
    response.raise_for_status()

    # La respuesta por defecto es un JSON con { "text": "Texto transcrito..." }
    result = response.json()
    return result["text"]
