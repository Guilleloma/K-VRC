import os
import time
from chat.chat_manager import get_chat_response, load_memory, save_memory
from face.oled_controller import OledFaceController
from chat.tts.tts_openai import OpenAITTS
from chat.stt.stt_main import transcribe_audio
from chat.sts.sts_speech import sts_speech
from led.led_controller import LEDController
from vision.camera import capture_camera_image, analyze_image
from audio.audio_controller import AudioPlayer
from chat.stt.stt_whisper_http import transcribe_file
from dotenv import load_dotenv
from config import LED_PIN  # Importamos la configuración del pin del LED

# Cargar variables de entorno del archivo .env
load_dotenv()

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
    
    # Inicializamos el controlador LED con el pin definido en config.py
    led = LEDController(pin=LED_PIN)
    
    try:
        # Encendemos el LED como señal visual
        led.turn_on()
        
        # Reproducimos 'hi.wav' para indicar que el sistema ha arrancado
        player.play_audio("hi.wav")
        
        # El LED permanece encendido como indicador de que el sistema está funcionando
    except Exception as e:
        print(f"Error al reproducir el audio de inicio: {e}")
        led.turn_off()  # Solo apagamos el LED si hay error

    # Reiniciamos la memoria SOLO al iniciar K-VRC
    reset_memory()
    
    # Cargamos la memoria después de haberla reiniciado
    chat_history = load_memory()

    # Inicializamos el controlador de la cara OLED
    face_controller = OledFaceController()
    face_controller.start_eyes_animation(interval_open=3.0, interval_blink=0.1)

    # Inicializamos el cliente TTS
    tts_client = OpenAITTS()

    print("=== K-VRC Conversational ===")
    print("Presiona Ctrl+C para salir.\n")

    try:
        while True:
            # El LED permanece encendido mientras esperamos
            print("🎙️ Escuchando... (Habla y luego guarda silencio)")
            
            # Obtener transcripción de voz a texto
            result_text = transcribe_audio()

            # Verificar que haya texto antes de continuar
            if not result_text:
                print("⚠️ No se obtuvo texto válido. Intentando nuevamente...")
                continue

            print("=== Transcripción ===")
            print(result_text)
            print("=====================\n")

            # Si se solicita describir lo que "ve" el robot
            if "lo que ves" in result_text.lower() or "qué ves" in result_text.lower():
                try:
                    print("🚀 Capturando imagen de la cámara para analizar lo que veo...")
                    image_path = capture_camera_image()
                    if image_path:
                        analysis_result = analyze_image(image_path)
                        response_text = "Esto es lo que veo: " + str(analysis_result)
                        print("=== Respuesta de análisis de imagen ===")
                        print(response_text)
                        
                        # Preparamos animación para responder
                        face_controller.stop_eyes_animation()
                        face_controller.start_mouth_animation(interval_mouth=0.2)
                        
                        # Generamos y reproducimos la respuesta
                        tts_client.texto_a_voz_streaming(response_text, output_file="output.mp3")
                        
                        # Restauramos estado normal
                        face_controller.stop_mouth_animation()
                        face_controller.start_eyes_animation()
                    else:
                        print("No se pudo capturar la imagen de la cámara.")
                except Exception as e:
                    print("Error al analizar la imagen:", e)
                continue

            # Obtener respuesta de GPT
            chat_response = get_chat_response(result_text, personality_file="personality_system.txt")
            print("=== Respuesta de K-VRC ===")
            print(chat_response)
            print("====================================\n")

            # Preparamos animación para responder
            face_controller.stop_eyes_animation()
            face_controller.start_mouth_animation(interval_mouth=0.2)

            # Generar y reproducir respuesta de texto a voz
            tts_client.texto_a_voz_streaming(chat_response, output_file="output.mp3")

            # Restauramos el estado normal
            face_controller.stop_mouth_animation()
            face_controller.start_eyes_animation()

            # Pequeña pausa antes de volver a escuchar
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("🛑 Interrumpido por el usuario. Saliendo...")
    finally:
        # Secuencia de apagado ordenada
        print("🔆 Finalizando y limpiando recursos...")
        
        # Aseguramos que todo queda apagado y limpio
        led.turn_off()
        led.cleanup()
        
        # Limpiar controlador de cara OLED
        face_controller.stop_eyes_animation()
        face_controller.stop_mouth_animation()
        face_controller.cleanup()

if __name__ == "__main__":
    main()
