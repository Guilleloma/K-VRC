import os
# Importación condicional de cv2
try:
    import cv2
    has_opencv = True
except ImportError:
    has_opencv = False
import time
import base64
import openai
import sys
import subprocess

# Aseguramos que se encuentre el módulo 'utils'
# Si ya configuraste PYTHONPATH, esta línea no sería necesaria
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import create_video_capture, is_raspberry_pi

def capture_camera_image(device_index=0, image_path="captured_image.jpg"):
    """
    Captura una imagen de la cámara y la guarda en un archivo.
    
    :param device_index: Índice del dispositivo de captura.
    :param image_path: Ruta donde se guardará la imagen capturada.
    :return: True si la captura fue exitosa, False en caso contrario.
    """
    print(f"[DEBUG] __file__ de camera.py: {__file__}")
    
    # Si no se especifica output_path, usar la carpeta del módulo
    if output_path is None:
        base_dir = os.path.dirname(os.path.realpath(__file__))
        output_path = os.path.join(base_dir, "captured_image.jpg")
        output_path = os.path.abspath(output_path)
        print(f"[DEBUG] Guardando imagen en: {output_path}")
    
    if is_raspberry_pi():
        # Uso del stack de libcamera en Raspberry Pi
        command = ["libcamera-still", "-o", output_path, "--nopreview", "-t", "2000"]
        print(f"[DEBUG] Ejecutando comando: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True)
        if result.returncode != 0:
            print("[ERROR] libcamera-still falló:", result.stderr.decode().strip())
            return None
        print(f"📸 Imagen capturada (con libcamera) guardada en {output_path}")
        return output_path
    else:
        # Uso del pipeline OpenCV como fallback en otros entornos
        cap = create_video_capture()
        if not cap.isOpened():
            print("Error: Could not open camera")
        return None

        # Reducir la resolución para disminuir la carga de memoria
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    if not has_opencv:
        print("OpenCV no está disponible. No se puede capturar imagen.")
        return False
        
    try:
        cap = create_video_capture(device_index)
        ret, frame = cap.read()
        
        if not ret:
            print("Error al capturar imagen.")
            return False
            
        cv2.imwrite(image_path, frame)
        cap.release()
        return True
    except Exception as e:
        print(f"Error al capturar imagen: {e}")
        return False

def analyze_image(image_path):
    """
    Analiza una imagen para determinar características básicas.
    
    :param image_path: Ruta de la imagen a analizar.
    :return: Un diccionario con los resultados del análisis o None si hay error.
    """
    if not has_opencv or not os.path.exists(image_path):
        print("OpenCV no está disponible o la imagen no existe.")
        return None
        
    try:
        image = cv2.imread(image_path)
        if image is None:
            print("No se pudo cargar la imagen.")
            return None
            
        # Análisis básico: dimensiones y valor promedio
        height, width = image.shape[:2]
        average_color = image.mean(axis=0).mean(axis=0)
        
        return {
            "width": width,
            "height": height,
            "average_color": average_color.tolist()
        }
    except Exception as e:
        print(f"Error al analizar imagen: {e}")
        return None

if __name__ == "__main__":
    image_path = capture_camera_image()
    if image_path:
        try:
            result = analyze_image(image_path)
            print("Análisis de la imagen:", result)
        except Exception as e:
            print("Error al analizar la imagen:", e)
