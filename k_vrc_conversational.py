import os
import time
from chat.chat_manager import get_chat_response, load_memory, save_memory  # Importamos memoria
from oled_controller import OledFaceController
from tts.tts_openai import OpenAITTS
from stt.stt_main import transcribe_audio  # Ahora solo importamos la transcripción

# Ruta corregida para la memoria
CHAT_MEMORY_DIR = "chat"
MEMORY_FILE = os.path.join(CHAT_MEMORY_DIR, "chat_memory.json")

def reset_memory():
    """Borra el archivo JSON al inicio del programa para reiniciar la memoria."""
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
        print("🔄 Memoria borrada al iniciar K-VRC.")

def main():
    # 🔹 Reiniciamos la memoria SOLO al iniciar K-VRC
    reset_memory()
    
    # 🔹 Cargamos la memoria después de haberla reiniciado
    chat_history = load_memory()

    face_controller = OledFaceController()
    face_controller.start_eyes_animation(interval_open=3.0, interval_blink=0.1)

    # Instanciamos nuestro TTS
    tts_client = OpenAITTS()  # Usa la API_KEY de la variable de entorno

    print("=== K-VRC Conversational ===")
    print("Presiona Ctrl+C para salir.\n")

    try:
        while True:
            print("🎙️ Escuchando... (Habla y luego guarda silencio)")
            
            # 1) Obtener transcripción de STT
            result_text = transcribe_audio()

            # 2) Verificar que haya texto antes de continuar
            if not result_text:
                print("⚠️ No se obtuvo texto válido. Intentando nuevamente...")
                continue

            print("=== Transcripción ===")
            print(result_text)
            print("=====================\n")

            # 3) Obtener respuesta de GPT
            chat_response = get_chat_response(result_text, personality_file="chat/personality_system.txt")
            print("=== Respuesta de K-VRC ===")
            print(chat_response)
            print("====================================\n")

            # 4) Simular el momento de "hablar"
            face_controller.stop_eyes_animation()
            face_controller.start_mouth_animation(interval_mouth=0.2)

            # 5) Llamar a TTS
            tts_client.texto_a_voz_streaming(chat_response, output_file="output.mp3")

            # 6) Parar boca y volver a ojos
            face_controller.stop_mouth_animation()
            face_controller.start_eyes_animation()

            time.sleep(1)

    except KeyboardInterrupt:
        print("🛑 Interrumpido por el usuario. Saliendo...")
    finally:
        face_controller.stop_eyes_animation()
        face_controller.stop_mouth_animation()
        face_controller.cleanup()

if __name__ == "__main__":
    main()
