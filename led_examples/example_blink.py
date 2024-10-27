import sys
import os

# Añadir el directorio padre al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from led_controller import LEDController
import time

def main():
    led_pin = 27  # Usa el pin GPIO 27
    led = LEDController(led_pin)
    
    try:
        print("Iniciando el efecto de parpadeo...")
        # Configura el parpadeo con 0.5 segundos encendido, 0.5 segundos apagado, repite 10 veces
        led.blink(0.5, 0.5, 10)
    finally:
        led.cleanup()
        print("Limpieza y apagado.")

if __name__ == "__main__":
    main()