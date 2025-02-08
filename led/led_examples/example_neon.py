import os
import sys
import time

print("Current directory:", os.getcwd())
print("Script location:", os.path.dirname(__file__))

# Se calcula el directorio raíz del proyecto (dos niveles arriba)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
print("Project root path:", project_root)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from led.led_controller import LEDController

def main():
    led_pin = 27  # Usa el pin GPIO según tu configuración
    led = LEDController(led_pin)
    
    try:
        print("Iniciando el efecto neón estropeado...")
        led.blink_neon_effect(10)  # Ejecuta el efecto neón por 10 segundos
    except KeyboardInterrupt:
        print("Interrumpido por el usuario.")
    finally:
        led.cleanup()
        print("Limpieza realizada y LED apagado.")

if __name__ == "__main__":
    main()