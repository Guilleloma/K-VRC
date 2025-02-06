import time
import os
import openai
from stt.audio_capture import RealTimeAudioCapture
from stt.stt_whisper_http import transcribe_file
from chat.chat_manager import get_chat_response
from oled_controller import OledFaceController
# === Importamos nuestra clase TTS de la carpeta 'tts' ===
from tts.tts_openai import OpenAITTS

def main():
    # Asegúrate que openai.api_key ya esté configurada (p.ej. con la variable de entorno)
    # o pásala directamente en la inicialización de OpenAITTS(api_key="...").
    
    face_controller = OledFaceController()
    face_controller.start_eyes_animation(interval_open=3.0, interval_blink=0.1)

    audio_capture = RealTimeAudioCapture(
        channels=1,
        rate=16000,
        chunk=1024,
        silence_threshold=20,
        silence_duration=2.0,
        output_path="temp_audio.wav"
    )

    # Instanciamos nuestro TTS
    tts_client = OpenAITTS()  # si la API_KEY está en variable de entorno, no pasamos nada
    # o: tts_client = OpenAITTS(api_key="AQUI_TU_CLAVE")

    print("=== K-VRC Conversational ===")
    print("Presiona Ctrl+C para salir.\n")

    try:
        while True:
            print("Escuchando... (Habla y luego guarda silencio)")
            audio_file_path = audio_capture.listen_and_record()

            # 1) Transcribir con Whisper
            print("Enviando audio a Whisper (OpenAI)...")
            result_text = transcribe_file(
                file_path=audio_file_path,
                language="es",
                temperature=0.0
            )
            print("=== Transcripción ===")
            print(result_text)
            print("=====================\n")

            # 2) Obtener respuesta GPT
            if result_text.strip():
                chat_response = get_chat_response(result_text, personality_file="chat/personality_system.txt")
                print("=== Respuesta de K-VRC ===")
                print(chat_response)
                print("====================================\n")

                # Simular el momento de "hablar"
                face_controller.stop_eyes_animation()
                face_controller.start_mouth_animation(interval_mouth=0.2)

                # 3) Llamar a TTS
                tts_client.texto_a_voz_streaming(chat_response, output_file="output.mp3")

                # 4) Parar boca y volver a ojos
                face_controller.stop_mouth_animation()
                face_controller.start_eyes_animation()
            else:
                print("No se obtuvo texto. Intenta de nuevo.")

            time.sleep(1)

    except KeyboardInterrupt:
        print("Interrumpido por el usuario. Saliendo...")
    finally:
        face_controller.stop_eyes_animation()
        face_controller.stop_mouth_animation()
        face_controller.cleanup()

if __name__ == "__main__":
    main()
