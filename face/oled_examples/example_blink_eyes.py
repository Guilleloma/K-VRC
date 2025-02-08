import os
import sys
import time

# Se agrega el directorio raíz del proyecto al sys.path,
# para que se puedan importar utils y demás módulos correctamente.
# Suponiendo que el directorio raíz es dos niveles arriba (ajusta según corresponda)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from face.oled_controller import OledFaceController

def main():
    print("Iniciando animación de parpadeo de ojos...")
    controller = OledFaceController()
    
    try:
        # Lanzamos la animación de ojos (definida en oled_controller.py)
        # Esta animación se ejecuta en un thread, por lo que dejamos correr el proceso
        controller.start_eyes_animation(interval_open=3.0, interval_blink=0.1)
        
        # Deja correr la animación durante 10 segundos para pruebas
        time.sleep(10)
    except KeyboardInterrupt:
        print("Interrumpido por el usuario.")
    finally:
        # Detenemos la animación de ojos y limpiamos el display
        controller.stop_eyes_animation()
        controller.cleanup()
        print("Animación detenida y display limpiado.")

if __name__ == "__main__":
    main()
