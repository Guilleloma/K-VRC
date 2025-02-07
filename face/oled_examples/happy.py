import sys
import os

# Añadir el directorio padre al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from face.oled_controller import OledFaceController

def main():
    oled = OledFaceController()
    
    try:
        oled.display_happy_image()  # Mostrar la imagen "Happy"
    except KeyboardInterrupt:
        oled.cleanup()

if __name__ == "__main__":
    main()