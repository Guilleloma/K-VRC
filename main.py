import os
import time
from chat.chat_manager import get_chat_response, load_memory, save_memory  # Importamos memoria
from face.oled_controller import OledFaceController
from tts.tts_openai import OpenAITTS
from stt.stt_main import transcribe_audio  # Ahora solo importamos la transcripción
from sts.sts_speech import sts_speech
from led.led_controller import LEDController  # Importamos el controlador del LED
from vision.camera import capture_camera_image, analyze_image  # Funciones para capturar y analizar imagen
from audio.audio_controller import AudioPlayer


# Ruta corregida para la memoria
CHAT_MEMORY_DIR = "chat"
MEMORY_FILE = os.path.join(CHAT_MEMORY_DIR, "chat_memory.json")

def reset_memory():
    """Borra el archivo JSON al inicio del programa para reiniciar la memoria."""
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
        print("🔄 Memoria borrada al iniciar K-VRC.")

def main():
    # Instanciamos el reproductor de audio
    player = AudioPlayer()
    try:
        # Reproducimos 'hi.wav' para indicar que el sistema ha arrancado
        player.play_audio("hi.wav")
    except Exception as e:
        print(f"Error al reproducir el audio de inicio: {e}")

    # 🔹 Reiniciamos la memoria SOLO al iniciar K-VRC
    reset_memory()
    
    # 🔹 Cargamos la memoria después de haberla reiniciado
    chat_history = load_memory()

    face_controller = OledFaceController()
    face_controller.start_eyes_animation(interval_open=3.0, interval_blink=0.1)

    # Instanciamos nuestro TTS (aunque aquí no lo estamos usando)
    tts_client = OpenAITTS()  # Usa la API_KEY de la variable de entorno

    # 🔹 Instanciamos y activamos el efecto FIRE del LED al iniciar el programa
    led = LEDController(pin=27)  # Asegúrate de que el pin es el correcto
    print("🔥 Iniciando efecto FIRE del LED...")
    led.fire_effect(duration=2)  # El efecto dura 10 segundos al inicio

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

            # 2) Si se solicita describir lo que "ve" el robot, se captura una imagen de la cámara
            if "lo que ves" in result_text.lower() or "qué ves" in result_text.lower():
                try:
                    print("🚀 Capturando imagen de la cámara para analizar lo que veo...")
                    image_path = capture_camera_image()
                    if image_path:
                        analysis_result = analyze_image(image_path)
                        response_text = "Esto es lo que veo: " + str(analysis_result)
                        print("=== Respuesta de análisis de imagen ===")
                        print(response_text)
                        tts_client.texto_a_voz_streaming(response_text, output_file="output.mp3")
                    else:
                        print("No se pudo capturar la imagen de la cámara.")
                except Exception as e:
                    print("Error al analizar la imagen:", e)
                continue

            # 3) Obtener respuesta de GPT
            chat_response = get_chat_response(result_text, personality_file="chat/personality_system.txt")
            print("=== Respuesta de K-VRC ===")
            print(chat_response)
            print("====================================\n")

            # 4) Simular el momento de "hablar"
            face_controller.stop_eyes_animation()
            face_controller.start_mouth_animation(interval_mouth=0.2)

            # 5) Llamar a STS (Speech-to-Speech) en tiempo real
            #sts_speech(chat_response)
            # Si prefieres usar TTS tradicional, descomenta la siguiente línea y comenta la línea de STS:
            tts_client.texto_a_voz_streaming(chat_response, output_file="output.mp3")

            # 6) Parar boca y volver a encender los ojos
            face_controller.stop_mouth_animation()
            face_controller.start_eyes_animation()

            time.sleep(1)

    except KeyboardInterrupt:
        print("🛑 Interrumpido por el usuario. Saliendo...")
    finally:
        print("🔆 Desactivando efecto y apagando LED...")
        led.blink_neon_effect(duration=2)  # Pequeño efecto antes de apagar
        led.turn_off()
        led.cleanup()
       
        # 🔹 Detener animaciones antes de salir
        face_controller.stop_eyes_animation()
        face_controller.stop_mouth_animation()
        face_controller.cleanup()

if __name__ == "__main__":
    main()
