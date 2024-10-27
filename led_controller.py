import RPi.GPIO as GPIO
import time
import random

class LEDController:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 1000)  # Configura PWM a 1kHz
        self.pwm.start(0)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()

    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def blink_neon_effect(self, duration):
        start_time = time.time()
        while time.time() - start_time < duration:
            on_time = random.uniform(0.05, 0.3)
            off_time = random.uniform(0.05, 0.3)
            self.turn_on()
            time.sleep(on_time)
            self.turn_off()
            time.sleep(off_time)
    
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