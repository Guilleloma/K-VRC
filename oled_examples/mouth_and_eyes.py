import sys
import os
import time
import threading
from queue import Queue


# Añadir el directorio padre al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oled_controller import OledFaceController  # Importa la clase OledFaceController desde tu módulo o archivo

def main():
    oled = OledFaceController()

    # Define los intervalos para el parpadeo de los ojos y el movimiento de la boca
    interval_open_eyes = 5
    interval_blink_eyes = 0.05  # Reducción para aumentar la fluidez de los ojos
    interval_move_mouth = 0.5  # Intervalo para el movimiento de la boca

    # Crea una cola para encolar las órdenes de cambio de imágenes
    image_queue = Queue()

    # Crea dos subprocesos para ejecutar las funciones de los ojos y la boca en paralelo
    thread_eyes = threading.Thread(target=oled.move_eyes_randomly, args=(interval_open_eyes, interval_blink_eyes))
    thread_mouth = threading.Thread(target=oled.move_mouth_continuously, args=(interval_move_mouth,))

    # Inicia los subprocesos
    thread_eyes.start()
    thread_mouth.start()

    try:
        while True:
            time.sleep(1)  # Espera indefinidamente, los subprocesos se encargan del resto

    except KeyboardInterrupt:
        oled.cleanup()

if __name__ == "__main__":
    main()
