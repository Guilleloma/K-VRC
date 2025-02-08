import os
import sys
import time

# Se agrega el directorio raíz del proyecto al sys.path,
# para que se puedan importar utils y demás módulos correctamente.
print("Current directory:", os.getcwd())
print("Script location:", os.path.dirname(__file__))

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
print("Project root path:", project_root)
print("sys.path before:", sys.path)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

print("sys.path after:", sys.path)

from face.oled_controller import OledFaceController

def main():
    print("Iniciando animación de ojos y boca...")
    controller = OledFaceController()
    
    try:
        # Iniciamos ambas animaciones
        controller.start_eyes_animation(interval_open=3.0, interval_blink=0.1)
        controller.start_mouth_animation(interval_mouth=0.2)
        
        # Dejamos que las animaciones corran durante 10 segundos
        time.sleep(10)
        
    except KeyboardInterrupt:
        print("Interrumpido por el usuario.")
    finally:
        # Detenemos ambas animaciones y limpiamos
        controller.stop_eyes_animation()
        controller.stop_mouth_animation()
        controller.cleanup()
        print("Animaciones detenidas y display limpiado.")

if __name__ == "__main__":
    main()
