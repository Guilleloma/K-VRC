import platform
import os

def is_raspberry_pi():
    """
    Detecta si el entorno es una Raspberry Pi.
    Se asume que en Raspberry Pi existe el archivo '/proc/cpuinfo' y
    que contiene cadenas específicas (como 'BCM' o 'Raspberry Pi').
    """
    if platform.system() == "Linux":
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()
            if "BCM" in cpuinfo or "Raspberry Pi" in cpuinfo:
                return True
        except Exception:
            return False
    return False
