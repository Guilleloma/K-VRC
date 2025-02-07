import os
import sys

# Agregar directorio padre al path (solución temporal)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from utils import is_raspberry_pi
except ImportError:
    # Definir una versión dummy de is_raspberry_pi si no existe
    def is_raspberry_pi():
        return False

if is_raspberry_pi():
    import RPi.GPIO as GPIO
else:
    print("No se detecta Raspberry Pi: usando controlador GPIO simulado.")
    class DummyGPIO:
        BCM = "BCM"
        OUT = "OUT"
        
        def setmode(self, mode):
            print(f"DummyGPIO: setmode({mode})")
            
        def setup(self, pin, mode):
            print(f"DummyGPIO: setup(pin={pin}, mode={mode})")
            
        def PWM(self, pin, frequency):
            print(f"DummyGPIO: creando PWM en el pin {pin} con frecuencia {frequency}Hz")
            class DummyPWM:
                def start(self, duty_cycle):
                    print(f"DummyPWM: iniciando con duty_cycle={duty_cycle}%")
                    
                def ChangeDutyCycle(self, duty_cycle):
                    print(f"DummyPWM: cambiando duty_cycle a {duty_cycle}%")
                    
                def stop(self):
                    print("DummyPWM: deteniendo PWM")
            return DummyPWM()
        
        def cleanup(self):
            print("DummyGPIO: limpiando configuración GPIO")
    
    GPIO = DummyGPIO()

import time
import random

class LEDController:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 100)  # Configura el PWM a 100Hz
        self.pwm.start(0)  # Inicia el PWM con ciclo de trabajo 0%

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()

    def turn_on(self):
        """
        Enciende el LED al 100% ajustando el ciclo del PWM.
        """
        self.pwm.ChangeDutyCycle(100)
        print("LED encendido al 100% de brillo.")

    def turn_off(self):
        """
        Apaga el LED ajustando el ciclo del PWM a 0%.
        """
        self.pwm.ChangeDutyCycle(0)
        print("LED apagado.")

    def dim(self, duty_cycle=10):
        """
        Atenúa el LED configurando un ciclo de trabajo bajo.
        
        :param duty_cycle: Porcentaje del ciclo de trabajo para atenuar (por defecto es 10%).
        """
        self.pwm.ChangeDutyCycle(duty_cycle)
        print(f"LED atenuado a {duty_cycle}% de brillo.")

    def blink_neon_effect(self, duration):
        """
        Crea un efecto de parpadeo similar a un neón al encender el LED por largos periodos
        con breves parpadeos de atenuación.
        
        :param duration: Tiempo total en segundos que durará el efecto.
        """
        start_time = time.time()
        while time.time() - start_time < duration:
            on_time = random.uniform(0.5, 1)
            flicker_time = random.uniform(0.05, 0.5)
            
            self.turn_on()
            time.sleep(on_time)
            
            self.dim(10)  # Atenúa brevemente el LED
            time.sleep(flicker_time)
        
    def blink(self, on_time, off_time, repeat):
        for _ in range(repeat):
            self.turn_on()
            time.sleep(on_time)
            self.turn_off()
            time.sleep(off_time)

    def fade(self, duration):
        start_time = time.time()
        while time.time() - start_time < duration:
            for duty_cycle in range(0, 101, 5):  # Incrementa el brillo
                self.pwm.ChangeDutyCycle(duty_cycle)
                time.sleep(0.05)
            for duty_cycle in range(100, -1, -5):  # Decrementa el brillo
                self.pwm.ChangeDutyCycle(duty_cycle)
                time.sleep(0.05)

    def fire_effect(self, duration):
        start_time = time.time()
        while time.time() - start_time < duration:
            intensity = random.uniform(0, 100)
            self.pwm.ChangeDutyCycle(intensity)
            time.sleep(random.uniform(0.05, 0.2))

# Ejemplo de uso
if __name__ == "__main__":
    led_pin = 27  # Pin GPIO
    led = LEDController(led_pin)
    
    try:
        print("Iniciando efecto FIRE...")
        led.fire_effect(duration=10)  # Efecto de 10 segundos
    except KeyboardInterrupt:
        print("Efecto interrumpido por el usuario.")
    finally:
        led.cleanup()
        print("Limpieza de LED finalizada.")
