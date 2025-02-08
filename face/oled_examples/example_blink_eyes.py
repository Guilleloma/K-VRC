import sys
import os

# Se asume que este archivo está dentro de 'face'; agregamos el directorio padre al sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from face.oled_controller import OledFaceController


def main():
    oled = OledFaceController()
    
    # Define los intervalos para el parpadeo de los ojos
    interval_open_eyes = 3
    interval_blink_eyes = 0.05  # Reducción para aumentar la fluidez de los ojos
    
    try:
        oled.move_eyes_randomly(interval_open_eyes, interval_blink_eyes)
    except KeyboardInterrupt:
        oled.cleanup()

if __name__ == "__main__":
    main()
