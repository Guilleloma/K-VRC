import RPi.GPIO as GPIO 
import time
import random

class LEDController:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 100)  # Configure PWM at 100Hz
        self.pwm.start(0)  # Start PWM with duty cycle 0%

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()

    def turn_on(self):
        """
        Turns the LED fully on by setting PWM duty cycle to 100%.
        """
        self.pwm.ChangeDutyCycle(100)
        print("LED turned ON at 100% brightness.")

    def turn_off(self):
        """
        Turns the LED fully off by setting PWM duty cycle to 0%.
        """
        self.pwm.ChangeDutyCycle(0)
        print("LED turned OFF.")

    def dim(self, duty_cycle=10):
        """
        Dims the LED by setting PWM duty cycle to a low value.
        
        :param duty_cycle: The duty cycle percentage for dimming (default is 10%).
        """
        self.pwm.ChangeDutyCycle(duty_cycle)
        print(f"LED dimmed to {duty_cycle}% brightness.")

    def blink_neon_effect(self, duration):
        """
        Creates a flickering neon effect by keeping the LED on for longer periods
        with brief dim flickers.
        
        :param duration: Total time in seconds for the effect to run.
        """
        start_time = time.time()
        while time.time() - start_time < duration:
            # Longer on-time between 0.5 to 1.5 seconds
            on_time = random.uniform(0.5, 1)
            # Short flicker dim-time between 0.05 to 0.2 seconds
            flicker_time = random.uniform(0.05, 0.5)
            
            self.turn_on()
            time.sleep(on_time)
            
            self.dim(10)  # Dim the LED briefly
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
            for duty_cycle in range(0, 101, 5):  # Increase brightness
                self.pwm.ChangeDutyCycle(duty_cycle)
                time.sleep(0.05)
            for duty_cycle in range(100, -1, -5):  # Decrease brightness
                self.pwm.ChangeDutyCycle(duty_cycle)
                time.sleep(0.05)

    def fire_effect(self, duration):
        start_time = time.time()
        while time.time() - start_time < duration:
            intensity = random.uniform(0, 100)
            self.pwm.ChangeDutyCycle(intensity)
            time.sleep(random.uniform(0.05, 0.2))

# Example usage
if __name__ == "__main__":
    led_pin = 27  # Example GPIO pin
    led = LEDController(led_pin)
    
    try:
        print("Starting neon effect...")
        led.blink_neon_effect(duration=30)  # Run the effect for 30 seconds
    except KeyboardInterrupt:
        print("Effect interrupted by user.")
    finally:
        led.cleanup()
        print("LED cleanup done.")
