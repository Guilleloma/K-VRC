import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image

# Define los pines I2C
RST = None     # en las pantallas más nuevas, RST puede ser None
I2C_ADDRESS = 0x3C

# Inicializa la pantalla con I2C
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Inicializa la biblioteca, debe ser llamada antes de cualquier otro comando.
disp.begin()

# Limpia la pantalla.
disp.clear()
disp.display()

# Carga una imagen desde un archivo.
image = Image.open('image.bmp').convert('1')

# Asegúrate de que la imagen tenga el tamaño correcto (128x64 píxeles)
image = image.resize((128, 64))

# Muestra la imagen en la pantalla OLED
disp.image(image)
disp.display()

# Mantén la imagen en la pantalla
time.sleep(10)  # Mantiene la imagen visible por 10 segundos