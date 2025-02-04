# k_vrc_conversational.py
import time
import os

# Importamos tu lógica de STT
from stt.audio_capture import RealTimeAudioCapture
from stt.stt_whisper_http import transcribe_file

# Importamos la parte de Chat (con personalidad)
from chat.chat_manager import get_chat_response

def main():
    # Configuramos el capturador de audio con los mismos parámetros que en stt_main.py (o los que prefieras).
    audio_capture = RealTimeAudioCapture(
        channels=1,
        rate=16000,
        chunk=1024,
        silence_threshold=20,
        silence_duration=2.0,
        output_path="temp_audio.wav"
    )

    print("=== K-VRC Conversational ===")
    print("Presiona Ctrl+C para salir.\n")

    try:
        while True:
            print("Escuchando... (Habla y luego guarda silencio para transcribir)")
            
            # 1) Capturamos audio hasta silencio
            audio_file_path = audio_capture.listen_and_record()

            # 2) Enviamos el audio a Whisper
            print("Enviando audio a OpenAI Whisper...")
            result_text = transcribe_file(
                file_path=audio_file_path,
                language="es",
                temperature=0.0
            )

            print("=== Transcripción ===")
            print(result_text)
            print("=====================\n")

            # 3) Con el texto transcrito, llamamos a ChatGPT (K-VRC)
            if result_text.strip():
                chat_response = get_chat_response(result_text, personality_file="chat/personality_system.txt")

                print("=== Respuesta de K-VRC ===")
                print(chat_response)
                print("====================================\n")

                # 4) (Opcional) Podrías hacer TTS, mover servos, etc.

            else:
                print("No se obtuvo texto. Intenta de nuevo.")

            # 5) (Opcional) Eliminar temp_audio.wav
            # os.remove(audio_file_path)

            time.sleep(1)

    except KeyboardInterrupt:
        print("Interrumpido por el usuario. Saliendo...")

if __name__ == "__main__":
    main()
