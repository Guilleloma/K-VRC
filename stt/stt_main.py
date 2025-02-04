# stt_main.py
import os
import time
from audio_capture import RealTimeAudioCapture
from stt_whisper_http import transcribe_file  # <-- Importamos nuestra nueva función

def main():
    # Instanciamos el capturador de audio
    audio_capture = RealTimeAudioCapture(
        channels=1,
        rate=16000,
        chunk=1024,
        silence_threshold=20,
        silence_duration=2.0,
        output_path="temp_audio.wav"
    )

    print("¡Iniciando loop de escucha y transcripción!\nPresiona Ctrl+C para salir.\n")

    try:
        while True:
            print("Escuchando... (Habla y luego guarda silencio para transcribir)")
            
            # 1. Escuchamos hasta silencio, guardamos en WAV
            audio_file_path = audio_capture.listen_and_record()

            # 2. Mandamos a OpenAI Whisper
            print("Enviando audio a OpenAI Whisper (endpoint /v1/audio/transcriptions)...")
            result_text = transcribe_file(
                file_path=audio_file_path,
                language="es",
                temperature=0.0
            )

            # 3. Mostramos el resultado
            print("================================")
            print(f"Transcripción:\n{result_text}")
            print("================================\n")

            # 4. (Opcional) Borrar el wav temporal
            # os.remove(audio_file_path)

            time.sleep(1)

    except KeyboardInterrupt:
        print("Interrumpido por el usuario. Saliendo...")

if __name__ == "__main__":
    main()
