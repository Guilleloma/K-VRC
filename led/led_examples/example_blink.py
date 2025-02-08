import os
import sys
import time

# Calcular el directorio raíz del proyecto:
# Desde este archivo (K-VRC/led/led_examples/example_blink.py),
# subimos dos niveles hasta K-VRC.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
print("Project root:", project_root)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Importa el LEDController desde el paquete led
from led.led_controller import LEDController

def main():
    print("Iniciando ejemplo blink LED...")
    led_pin = 27  # Asigna el pin GPIO de acuerdo a tu configuración
    led = LEDController(led_pin)

    try:
        # Ejemplo: parpadeo del LED 10 veces con intervalos de 0.5 segundos
        led.blink(0.5, 0.5, 10)
    except KeyboardInterrupt:
        print("Interrumpido por el usuario.")
    finally:
        led.cleanup()
        print("Limpieza realizada.")

if __name__ == "__main__":
    main()