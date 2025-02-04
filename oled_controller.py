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

        # ============ FLAGS Y THREADS DE ANIMACIÓN ============
        self.eyes_running = False
        self.mouth_running = False
        self.eyes_thread = None
        self.mouth_thread = None

    def load_image(self, filename):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, 'images', filename)
        # Ajusta el tamaño según tu diseño: (128,32) para ojos y (128,32) para boca, etc.
        return Image.open(image_path).convert('1').resize((128, 32))

    def display_images(self):
        """
        Hilo permanente que toma (eye_image, mouth_image) de la cola y
        dibuja la cara completa en la pantalla (ojos arriba, boca abajo).
        """
        while True:
            eye_image, mouth_image = self.image_queue.get()
            full_image = Image.new('1', (self.disp.width, self.disp.height))
            # Pegar ojos en la mitad superior
            full_image.paste(eye_image, (0, 0))
            # Pegar boca en la mitad inferior
            full_image.paste(mouth_image, (0, self.disp.height // 2))

            self.disp.image(full_image)
            self.disp.display()

    def start_display_thread(self):
        display_thread = threading.Thread(target=self.display_images, daemon=True)
        display_thread.start()

    # =================================================
    # =============== ANIMACIÓN DE OJOS ===============
    # =================================================
    def _eyes_loop(self, interval_open=3.0, interval_blink=0.1):
        """
        Bucle infinito que parpadea: varios estados en secuencia.
        Se detiene cuando self.eyes_running = False.
        """
        eye_sequence = ['half_open', 'half_closed', 'closed', 'half_closed', 'half_open','open']

        while self.eyes_running:
            # Escogemos un tiempo random que los ojos estarán "abiertos" antes de parpadear
            open_interval = random.uniform(interval_open - 1, interval_open + 1)

            # Realizar la secuencia de parpadeo
            for eye_state in eye_sequence:
                if not self.eyes_running:
                    break  # Si se ha detenido, salimos del for
                eye_image = self.eye_images[eye_state]
                mouth_image = self.mouth_images['closed']  # En reposo, boca cerrada
                self.image_queue.put((eye_image, mouth_image))
                time.sleep(interval_blink)

            # Esperar un rato (ojos abiertos) antes del siguiente parpadeo
            # Rompemos también si se desactiva el flag en medio
            elapsed = 0
            while elapsed < open_interval and self.eyes_running:
                time.sleep(0.1)
                elapsed += 0.1

        # Cuando salimos del bucle, dejamos una imagen final si queremos
        # Ojos abiertos y boca cerrada
        final_eye = self.eye_images['open']
        final_mouth = self.mouth_images['closed']
        self.image_queue.put((final_eye, final_mouth))

    def start_eyes_animation(self, interval_open=3.0, interval_blink=0.1):
        """Arranca la animación de ojos en un thread."""
        if self.eyes_running:
            return  # Ya está corriendo
        self.eyes_running = True
        self.eyes_thread = threading.Thread(
            target=self._eyes_loop,
            args=(interval_open, interval_blink),
            daemon=True
        )
        self.eyes_thread.start()

    def stop_eyes_animation(self):
        """Detiene la animación de ojos con el flag y espera a que termine el thread."""
        if not self.eyes_running:
            return
        self.eyes_running = False
        if self.eyes_thread:
            self.eyes_thread.join()
            self.eyes_thread = None

    # =================================================
    # ============== ANIMACIÓN DE BOCA ================
    # =================================================
    def _mouth_loop(self, interval_mouth=0.2):
        """
        Bucle infinito para animar la boca mientras habla.
        Se detiene cuando self.mouth_running = False.
        """
        while self.mouth_running:
            # Escoge un frame aleatorio de boca
            mouth_image = self.mouth_images[random.choice(list(self.mouth_images.keys()))]
            # Durante el habla, puedes mantener ojos 'open' o hacerlos parpadear, a gusto
            eye_image = self.eye_images['open']
            self.image_queue.put((eye_image, mouth_image))
            time.sleep(interval_mouth)

        # Al terminar, si quieres, dejas los ojos abiertos y boca cerrada
        final_eye = self.eye_images['open']
        final_mouth = self.mouth_images['closed']
        self.image_queue.put((final_eye, final_mouth))

    def start_mouth_animation(self, interval_mouth=0.2):
        """Arranca la animación de boca en un thread."""
        if self.mouth_running:
            return
        self.mouth_running = True
        self.mouth_thread = threading.Thread(
            target=self._mouth_loop,
            args=(interval_mouth,),
            daemon=True
        )
        self.mouth_thread.start()

    def stop_mouth_animation(self):
        """Detiene la animación de boca con el flag y espera a que termine el thread."""
        if not self.mouth_running:
            return
        self.mouth_running = False
        if self.mouth_thread:
            self.mouth_thread.join()
            self.mouth_thread = None

    # =================================================
    # =========== OTRAS IMÁGENES COMPLETAS ============
    # =================================================
    def display_wtf_image(self):
        """Carga y muestra una imagen de 'wtf.bmp' en 128x64."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, 'images', 'wtf.bmp')
        wtf_image = Image.open(image_path).convert('1').resize((128, 64))
        self.disp.image(wtf_image)
        self.disp.display()

    def display_happy_image(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, 'images', 'happy.bmp')
        happy_image = Image.open(image_path).convert('1').resize((128, 64))
        self.disp.image(happy_image)
        self.disp.display()

    def cleanup(self):
        """Limpieza final."""
        self.disp.clear()
        self.disp.display()
