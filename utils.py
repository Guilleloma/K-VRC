import platform
import os
import cv2

def is_raspberry_pi():
    """
    Determina si el código se está ejecutando en una Raspberry Pi.

    Intenta leer el archivo '/proc/device-tree/model', que existe en las Raspberry Pi,
    y verifica si en su contenido aparece la cadena 'raspberry pi'.
    
    :return: True si se detecta Raspberry Pi, False en caso contrario.
    """
    try:
        with open('/proc/device-tree/model', 'r') as model_file:
            model = model_file.read().lower()
            return 'raspberry pi' in model
    except Exception:
        return False

def create_video_capture(device_index=0):
    """
    Crea y retorna un objeto cv2.VideoCapture con el backend adecuado
    según el sistema operativo.

    En macOS se utilizará el backend por defecto de OpenCV, mientras que
    en sistemas Linux (como la Raspberry Pi) se forzará el uso de V4L2.

    :param device_index: Índice del dispositivo de captura (por defecto 0).
    :return: Instancia de cv2.VideoCapture.
    """
    if platform.system() == "Darwin":
        # En macOS, usar el backend por defecto
        return cv2.VideoCapture(device_index)
    else:
        # En Linux (ej. Raspberry Pi), forzar el backend V4L2
        return cv2.VideoCapture(device_index, cv2.CAP_V4L2)

# Aquí podrías agregar otras funciones dummy o de simulación si fuera necesario
# Por ejemplo, dummy para otros dispositivos:
#
# def create_dummy_device():
#     # Retorna una instancia dummy o simulada de un dispositivo
#     pass