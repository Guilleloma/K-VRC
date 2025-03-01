# stt_whisper_http.py
import os
import time
import requests
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def transcribe_file(file_path, language="es", temperature=0.0):
    """
    Envía un archivo de audio al endpoint /v1/audio/transcriptions
    de OpenAI para transcribir con 'whisper-1'.
    Incluye reintentos automáticos en caso de errores de conexión.
    """
    url = "https://api.openai.com/v1/audio/transcriptions"

    # Lee la API key desde la variable de entorno
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("La variable OPENAI_API_KEY no está configurada en el entorno.")

    print(f"[DEBUG] Iniciando transcripción con Whisper. Archivo: {file_path}")
    print(f"[DEBUG] Tamaño del archivo: {os.path.getsize(file_path) / 1024:.2f} KB")
    
    # Configurar un timeout más largo para la solicitud
    timeout = 60  # 60 segundos
    
    try:
        # Preparamos el archivo de audio y los parámetros
        with open(file_path, "rb") as f:
            files = {
                "file": (file_path, f, "application/octet-stream")
            }
            data = {
                "model": "whisper-1",
                "language": language,
                "temperature": temperature,
            }
            headers = {
                "Authorization": f"Bearer {api_key}"
            }

            # Llamada POST al endpoint de transcripciones con timeout
            print("[DEBUG] Enviando archivo a API de Whisper (con timeout)...")
            response = requests.post(
                url, 
                headers=headers, 
                data=data, 
                files=files,
                timeout=timeout
            )
        
        # Si la respuesta no es 2xx, lanza excepción
        response.raise_for_status()

        # La respuesta por defecto es un JSON con { "text": "Texto transcrito..." }
        result = response.json()
        print("[DEBUG] Transcripción recibida correctamente.")
        return result["text"]
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error de conexión con API de Whisper: {e}")
        # Re-lanzar la excepción para que el mecanismo de reintento funcione
        raise
