import sys
import os

# Añadir el directorio padre al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oled_face import OledFaceController

def main():
    oled = OledFaceController()
    
    try:
        oled.display_wtf_image()  # Mostrar la imagen "WTF"
    except KeyboardInterrupt:
        oled.cleanup()

if __name__ == "__main__":
    main()