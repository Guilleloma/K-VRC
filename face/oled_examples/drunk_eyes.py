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
    print("Mostrando ojos borrachos...")
    controller = OledFaceController()
    
    try:
        # Mostrar los ojos borrachos
        controller.display_drunk_eyes()
        
        # Esperar input del usuario para terminar
        input("Presiona Enter para salir...")
        
    except KeyboardInterrupt:
        print("Interrumpido por el usuario.")
    finally:
        controller.cleanup()
        print("Display limpiado.")

if __name__ == "__main__":
    main() 