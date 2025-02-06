import os
import wave
import numpy as np
from stt.stt_whisper_http import transcribe_file
from stt.audio_capture import RealTimeAudioCapture

def is_audio_speech(file_path, silence_threshold=12):
    """
    Verifica si el audio grabado contiene voz real o solo ruido de fondo/silencio.
    """
    with wave.open(file_path, 'rb') as wf:
        num_frames = wf.getnframes()
        audio_data = wf.readframes(num_frames)
        audio_np = np.frombuffer(audio_data, dtype=np.int16)

        # Calculamos el RMS promedio
        rms_value = np.sqrt(np.mean(audio_np.astype(np.float64) ** 2))
        print(f"🔊 RMS promedio del audio grabado: {rms_value}")

        return rms_value >= silence_threshold  # True si hay voz, False si es solo ruido

def transcribe_audio():
    """
    Captura el audio y lo transcribe solo si hay voz.
    """
    audio_capture = RealTimeAudioCapture(
        channels=1,
        rate=16000,
        chunk=1024,
        silence_threshold=12,
        silence_duration=2.0,
        output_path="temp_audio.wav"
    )

    # Capturar audio
    audio_file_path = audio_capture.listen_and_record()

    # Verificar si el audio tiene voz
    if not is_audio_speech(audio_file_path, silence_threshold=12):
        print("🤫 Silencio detectado. No se enviará nada a Whisper.")
        return None  # No hay transcripción

    # Transcribir con Whisper
    print("📝 Enviando audio a OpenAI Whisper...")
    result_text = transcribe_file(file_path=audio_file_path, language="es", temperature=0.0)

    return result_text.strip() if result_text.strip() else None
