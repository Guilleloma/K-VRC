import os
import random
from PIL import Image
import Adafruit_SSD1306
import time
import threading
from queue import Queue

class OledFaceController:
    def __init__(self):
        # Inicializar la pantalla OLED
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
        self.disp.begin()
        self.disp.clear()
        self.disp.display()

        # Cargar las imágenes de los ojos
        self.eye_images = {
            'open': self.load_image('eyes_open.bmp'),
            'half_open': self.load_image('eyes_half_open.bmp'),
            'half_closed': self.load_image('eyes_half_closed.bmp'),
            'closed': self.load_image('eyes_closed.bmp'),
        }

        # Cargar las imágenes de la boca
        self.mouth_images = {
            'open': self.load_image('mouth_open.bmp'),
            'closed': self.load_image('mouth_closed.bmp'),
            'half_open': self.load_image('mouth_half_open.bmp'),
        }

        # Crear una cola para controlar el acceso a la pantalla
        self.image_queue = Queue()

        # Iniciar el hilo para mostrar las imágenes en la pantalla
        self.start_display_thread()

    def load_image(self, filename):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, 'images', filename)
        return Image.open(image_path).convert('1').resize((128, 32))

    def move_eyes_randomly(self, interval_open, interval_blink):
        eye_sequence = ['half_open', 'half_closed', 'closed', 'half_closed', 'half_open','open']
        while True:
            open_interval = random.uniform(interval_open - 1, interval_open + 1)
            for eye_state in eye_sequence:
                eye_image = self.eye_images[eye_state]
                mouth_image = self.mouth_images['closed']  # Boca fija
                self.image_queue.put((eye_image, mouth_image))
                time.sleep(interval_blink)
            time.sleep(open_interval)

    def move_mouth_continuously(self, interval_mouth):
        while True:
            mouth_image = self.mouth_images[random.choice(list(self.mouth_images.keys()))]
            eye_image = self.eye_images['open']  # Mantén los ojos abiertos para suavizar
            self.image_queue.put((eye_image, mouth_image))
            time.sleep(interval_mouth)

    def display_images(self):
        while True:
            eye_image, mouth_image = self.image_queue.get()
            full_image = Image.new('1', (self.disp.width, self.disp.height))
            full_image.paste(eye_image, (0, 0))
            full_image.paste(mouth_image, (0, self.disp.height // 2))
            self.disp.image(full_image)
            self.disp.display()

    def start_display_thread(self):
        display_thread = threading.Thread(target=self.display_images)
        display_thread.daemon = True
        display_thread.start()

    def display_wtf_image(self):
        """Carga y muestra una imagen de 'wtf.bmp' de tamaño 128x64."""
        wtf_image = self.load_image('wtf.bmp').resize((128, 64))
        self.disp.image(wtf_image)
        self.disp.display()

    def display_happy_image(self):
        # Mostrar la imagen "happy.bmp" en la pantalla OLED
        happy_image = self.load_image('happy.bmp').resize((128, 64))
        self.disp.image(happy_image)
        self.disp.display()

    def cleanup(self):
        self.disp.clear()
        self.disp.display()
