import os
import sys
import glob
import importlib.util
import time

# Se agrega el directorio raíz del proyecto al sys.path
print("Current directory:", os.getcwd())
print("Script location:", os.path.dirname(__file__))

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
print("Project root path:", project_root)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from face.oled_controller import OledFaceController

def main():
    print("Iniciando demostración de ejemplos OLED...")
    controller = OledFaceController()
    
    try:
        # 1. Imagen feliz (5 segundos)
        print("\n1. Mostrando cara feliz")
        controller.cleanup()  # Limpiamos antes de mostrar la imagen
        time.sleep(0.2)
        controller.display_happy_image()
        time.sleep(5)
        controller.cleanup()
        time.sleep(0.5)
        
        # 2. Imagen WTF (5 segundos)
        print("\n2. Mostrando cara WTF")
        controller.display_wtf_image()
        time.sleep(5)
        controller.cleanup()
        time.sleep(0.5)
        
        # 3. Ojos borrachos (5 segundos)
        print("\n3. Mostrando ojos borrachos")
        controller.display_drunk_eyes()
        time.sleep(5)
        controller.cleanup()
        time.sleep(1)  # Pausa más larga antes de las animaciones

        # 4. Ejemplo de ojos parpadeantes (5 segundos)
        print("\n4. Demostración de parpadeo")
        controller.cleanup()
        time.sleep(0.5)  # Asegurar que el display está limpio
        controller.start_eyes_animation(interval_open=3.0, interval_blink=0.1)
        time.sleep(5)
        controller.stop_eyes_animation()
        time.sleep(0.5)  # Esperar a que el thread se detenga
        controller.cleanup()
        time.sleep(1)  # Pausa más larga entre animaciones
        
        # 5. Ejemplo de boca en movimiento (5 segundos)
        print("\n5. Demostración de boca")
        controller.cleanup()
        time.sleep(0.5)
        controller.start_mouth_animation(interval_mouth=0.2)
        time.sleep(5)
        controller.stop_mouth_animation()
        time.sleep(0.5)
        controller.cleanup()
        time.sleep(1)
        
        # 6. Ejemplo de ojos y boca simultáneos (5 segundos)
        print("\n6. Demostración de ojos y boca")
        controller.cleanup()
        time.sleep(0.5)
        controller.start_eyes_animation()
        controller.start_mouth_animation()
        time.sleep(5)
        controller.stop_eyes_animation()
        controller.stop_mouth_animation()
        time.sleep(0.5)
        controller.cleanup()
        
    except KeyboardInterrupt:
        print("\nDemostración interrumpida por el usuario.")
    finally:
        # Asegurarse de detener todas las animaciones y limpiar
        controller.stop_eyes_animation()
        controller.stop_mouth_animation()
        time.sleep(0.5)  # Esperar a que los threads se detengan
        controller.cleanup()
        print("\nDemostración completada y display limpiado.")

if __name__ == "__main__":
    main() 