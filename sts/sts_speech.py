
#Still not working

import asyncio
# Forzamos el uso del event loop por defecto
asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

# --- Monkey patch global a BaseEventLoop.create_connection ---
import ssl
import asyncio
_original_create_connection = asyncio.BaseEventLoop.create_connection

def _patched_create_connection(self, protocol_factory, *args, **kwargs):
    if "extra_headers" in kwargs:
        kwargs.pop("extra_headers")
    return _original_create_connection(self, protocol_factory, *args, **kwargs)

asyncio.BaseEventLoop.create_connection = _patched_create_connection
# ----------------------------------------------------------------

import json
import os
import websockets
import pyaudio

# Creamos un contexto SSL inseguro para pruebas
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

async def _sts_speech(text, model="gpt-4o-realtime-preview-2024-12-17", voice="alloy"):
    # URL de conexión según la documentación oficial
    websocket_url = "wss://api.openai.com/v1/realtime/sessions"
    
    # Encabezados de autenticación usando la API key
    headers = {
        "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}"
    }
    extra_headers = list(headers.items())

    # Conectarse con el contexto SSL personalizado
    async with websockets.connect(websocket_url, extra_headers=extra_headers, ssl=ssl_context) as ws:
        # Construir la solicitud (ajusta según la documentación)
        request = {
            "model": model,
            "modalities": ["audio"],
            "instructions": "Genera audio en tiempo real.",
            "voice": voice,
            "input_audio_format": "pcm16",
            "output_audio_format": "pcm16",
            "input": text
        }
        await ws.send(json.dumps(request))
        
        # Configurar PyAudio para la reproducción
        p = pyaudio.PyAudio()
        stream_out = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=22050,  # Ajusta la tasa según lo que devuelva la API
            output=True
        )
        
        print("[STS] Reproduciendo audio en tiempo real...")
        try:
            async for message in ws:
                stream_out.write(message)
        except websockets.exceptions.ConnectionClosed:
            pass

        stream_out.stop_stream()
        stream_out.close()
        p.terminate()
        print("[STS] Reproducción en tiempo real finalizada.")

def sts_speech(text, model="gpt-4o-realtime-preview-2024-12-17", voice="alloy"):
    asyncio.run(_sts_speech(text, model=model, voice=voice))

if __name__ == "__main__":
    sample_text = "Hola, este es un ejemplo de audio en tiempo real usando el Realtime API."
    sts_speech(sample_text)
