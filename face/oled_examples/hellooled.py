import os
import sys
import time
from PIL import Image

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
    print("Iniciando ejemplo Hello OLED...")
    controller = OledFaceController()
    
    try:
        # Carga una imagen desde un archivo
        image_path = os.path.join(os.path.dirname(__file__), 'image.bmp')
        image = Image.open(image_path).convert('1')
        
        # Asegúrate de que la imagen tenga el tamaño correcto (128x64 píxeles)
        image = image.resize((128, 64))
        
        # Muestra la imagen en la pantalla OLED
        controller.disp.image(image)
        controller.disp.display()
        
        # Mantén la imagen en la pantalla
        time.sleep(10)  # Mantiene la imagen visible por 10 segundos
        
    except KeyboardInterrupt:
        print("Interrumpido por el usuario.")
    finally:
        controller.cleanup()
        print("Display limpiado.")

if __name__ == "__main__":
    main()