# k_vrc_conversational.py
import time
import os

# Importamos nuestras clases y funciones de la carpeta stt
from stt.audio_capture import RealTimeAudioCapture
from stt.stt_whisper_http import transcribe_file

# Importamos la parte de ChatGPT
from chat.chat_manager import get_chat_response

def main():
    # Instanciamos el capturador de audio con los mismos parámetros que en stt_main.py
    audio_capture = RealTimeAudioCapture(
        channels=1,
        rate=16000,
        chunk=1024,
        silence_threshold=20,
        silence_duration=2.0,  # o el valor que uses
        output_path="temp_audio.wav"
    )

    print("=== K-VRC Conversational ===")
    print("Presiona Ctrl+C para salir.\n")

    try:
        while True:
            print("Escuchando... (Habla y luego guarda silencio para transcribir)")
            
            # 1) Capturar audio hasta que haya silencio
            audio_file_path = audio_capture.listen_and_record()

            # 2) Enviarlo a Whisper para transcripción
            print("Enviando audio a OpenAI Whisper...")
            result_text = transcribe_file(
                file_path=audio_file_path,
                language="es",
                temperature=0.0
            )

            print("=== Transcripción ===")
            print(result_text)
            print("=====================\n")

            # 3) Llamar a ChatGPT con la transcripción
            if result_text.strip():
                chat_response = get_chat_response(result_text)
                print("=== Respuesta de ChatGPT (K-VRC) ===")
                print(chat_response)
                print("====================================\n")

                # (Opcional) Aquí podrías hacer TTS, mover servos, etc.

            else:
                print("No se obtuvo texto. Intenta de nuevo.")

            # 4) Borrar el wav temporal si quieres
            # os.remove(audio_file_path)

            time.sleep(1)

    except KeyboardInterrupt:
        print("Interrumpido por el usuario. Saliendo...")

if __name__ == "__main__":
    main()
