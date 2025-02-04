# k_vrc_conversational.py
import time
import os

from stt.audio_capture import RealTimeAudioCapture
from stt.stt_whisper_http import transcribe_file
from chat.chat_manager import get_chat_response

# Importamos la clase con flags
from oled_controller import OledFaceController

def main():
    # Instanciamos el controlador de la cara
    face_controller = OledFaceController()

    # Arrancamos la animación de ojos (Idle)
    face_controller.start_eyes_animation(interval_open=3.0, interval_blink=0.1)

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
            audio_file_path = audio_capture.listen_and_record()

            # 1) Transcribir con Whisper
            print("Enviando audio a OpenAI Whisper...")
            result_text = transcribe_file(
                file_path=audio_file_path,
                language="es",
                temperature=0.0
            )

            print("=== Transcripción ===")
            print(result_text)
            print("=====================\n")

            # 2) Obtener respuesta de GPT
            if result_text.strip():
                chat_response = get_chat_response(result_text, personality_file="chat/personality_system.txt")

                print("=== Respuesta de K-VRC ===")
                print(chat_response)
                print("====================================\n")

                # Simular el momento de "hablar" (por TTS). 
                # AQUI paramos ojos y arrancamos boca
                face_controller.stop_eyes_animation()
                face_controller.start_mouth_animation(interval_mouth=0.2)

                # (Opcional) Si tuvieras TTS real, lo pones aquí. 
                # Aquí lo simulamos con un sleep de 3 segundos
                time.sleep(3)

                # Al terminar de "hablar", paramos la boca y volvemos a encender ojos
                face_controller.stop_mouth_animation()
                face_controller.start_eyes_animation()

            else:
                print("No se obtuvo texto. Intenta de nuevo.")

            time.sleep(1)

    except KeyboardInterrupt:
        print("Interrumpido por el usuario. Saliendo...")
    finally:
        # Asegurar detener animaciones y limpiar pantalla
        face_controller.stop_eyes_animation()
        face_controller.stop_mouth_animation()
        face_controller.cleanup()

if __name__ == "__main__":
    main()
