# servo/examples/casual_move_example.py

import sys
import os

# Añadir el directorio padre al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from servo_controller import ServoController
import time

def main():
    servo_pin = 12  # GPIO12
    servo = ServoController(servo_pin)
    
    try:
        servo.casual_move(min_angle=0, max_angle=180, min_delay=0.5, max_delay=1.5)
    except KeyboardInterrupt:
        print("Programa finalizado por el usuario.")
    finally:
        servo.cleanup()
        print("Limpieza y apagado.")

if __name__ == "__main__":
    main()
