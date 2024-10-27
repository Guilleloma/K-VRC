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
        print("Iniciando el efecto de desvanecimiento...")
        led.fade(10)  # Ejecuta el efecto de desvanecimiento por 10 segundos
    finally:
        led.cleanup()
        print("Limpieza y apagado.")

if __name__ == "__main__":
    main()