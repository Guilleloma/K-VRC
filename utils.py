import platform
import os
<<<<<<< Updated upstream
=======

# Modificar la importación de cv2 para que sea condicional
try:
    import cv2
    has_opencv = True
except ImportError:
    has_opencv = False
>>>>>>> Stashed changes

def is_raspberry_pi():
    """
    Determina si el código se está ejecutando en una Raspberry Pi.

    Intenta leer el archivo '/proc/device-tree/model', que existe en las Raspberry Pi,
    y verifica si en su contenido aparece la cadena 'raspberry pi'.
    
    :return: True si se detecta Raspberry Pi, False en caso contrario.
    """
    try:
        with open('/proc/device-tree/model', 'r') as f:
            model = f.read()
        return 'Raspberry Pi' in model
    except:
        # Fallback al método anterior si no podemos leer el modelo
        return platform.system() == 'Linux' and platform.machine().startswith(('arm', 'aarch'))

def create_video_capture(device_index=0):
    """
    Crea y retorna un objeto cv2.VideoCapture con el backend adecuado
    según el sistema operativo.

    En macOS se utilizará el backend por defecto de OpenCV, mientras que
    en sistemas Linux (como la Raspberry Pi) se forzará el uso de V4L2.

    :param device_index: Índice del dispositivo de captura (por defecto 0).
    :return: Instancia de cv2.VideoCapture.
    """
    import cv2  # Import moved here to avoid requiring it when not needed
    
    if platform.system() == "Darwin":
        # En macOS, usamos el backend por defecto
        return cv2.VideoCapture(device_index)
    else:
        # En Linux, usar el backend predeterminado en lugar de forzar V4L2
        return cv2.VideoCapture(device_index)