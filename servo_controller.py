# servo_controller.py

import RPi.GPIO as GPIO
import time
import random

class ServoController:
    def __init__(self, pin):
        """
        Inicializa el controlador del servo en el pin especificado.
        
        :param pin: Número de pin GPIO donde está conectado el servo.
        """
        self.pin = pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)  # Frecuencia de 50Hz para servos
        self.pwm.start(0)  # Posición inicial (90 grados)

    def cleanup(self):
        """
        Detiene el PWM y limpia la configuración de GPIO.
        """
        self.pwm.stop()
        GPIO.cleanup()

    def set_angle(self, angle):
        """
        Mueve el servo al ángulo especificado.

        :param angle: Ángulo al que mover el servo (0-180 grados).
        """
        duty = 2.5 + (angle / 180.0) * 10.0  # Mapeo del ángulo al duty cycle
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.05)
        #self.pwm.ChangeDutyCycle(0)
        print(f"Moviendo a {angle} grados (duty cycle: {duty}%)")

    def say_no(self, left_angle=30, right_angle=150, repetitions=5, delay=0.3):
        """
        Realiza un movimiento de "no", moviendo el servo rápidamente entre dos ángulos.
        
        :param left_angle: Ángulo hacia la izquierda.
        :param right_angle: Ángulo hacia la derecha.
        :param repetitions: Número de repeticiones del movimiento.
        :param delay: Pausa entre movimientos.
        """
        print("Realizando movimiento de 'No'")
        try:
            for _ in range(repetitions):
                self.set_angle(left_angle)
                time.sleep(delay)
                self.set_angle(right_angle)
                time.sleep(delay)
        except KeyboardInterrupt:
            print("Movimiento de 'No' detenido por el usuario.")
            

    def casual_move(self, min_angle=0, max_angle=180, min_delay=0.5, max_delay=1.5):
        """
        Realiza movimientos casuales moviendo el servo a ángulos aleatorios dentro de un rango.
        
        :param min_angle: Ángulo mínimo.
        :param max_angle: Ángulo máximo.
        :param min_delay: Tiempo mínimo de espera entre movimientos.
        :param max_delay: Tiempo máximo de espera entre movimientos.
        """
        print("Iniciando movimiento casual. Presiona Ctrl+C para detener.")
        try:
            while True:
                angle = random.randint(min_angle, max_angle)
                print(f"Configurando ángulo a {angle} grados")
                self.set_angle(angle)
                delay = random.uniform(min_delay, max_delay)
                print(f"Esperando {delay:.2f} segundos antes del siguiente movimiento")
                time.sleep(delay)
        except KeyboardInterrupt:
            print("Movimiento casual detenido por el usuario.")

    def calibrate(self):
        """
        Permite calibrar manualmente el servo ajustando el duty cycle.
        """
        print("Iniciando calibración del servo. Presiona Ctrl+C para salir.")
        try:
            while True:
                duty = float(input("Ingrese el duty cycle (0-100): "))
                self.pwm.ChangeDutyCycle(duty)
                time.sleep(0.5)
                self.pwm.ChangeDutyCycle(0)
                print(f"Duty cycle establecido a: {duty}%")
        except KeyboardInterrupt:
            print("Calibración finalizada por el usuario.")

    def sweep(self, start_angle=0, end_angle=180, step=1, delay=0.05):
        """
        Realiza un barrido de ángulos de start_angle a end_angle y viceversa.

        :param start_angle: Ángulo inicial del barrido.
        :param end_angle: Ángulo final del barrido.
        :param step: Incremento de ángulo en cada paso.
        :param delay: Pausa entre movimientos.
        """
        print(f"Iniciando barrido de {start_angle} a {end_angle} grados.")
        try:
            while True:
                for angle in range(start_angle, end_angle + 1, step):
                    self.set_angle(angle)
                    time.sleep(delay)
                for angle in range(end_angle, start_angle - 1, -step):
                    self.set_angle(angle)
                    time.sleep(delay)
        except KeyboardInterrupt:
            print("Barrido detenido por el usuario.")
