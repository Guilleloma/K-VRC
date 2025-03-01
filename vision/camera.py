import os
import cv2
import time
import base64
import openai
import sys
import subprocess

# Aseguramos que se encuentre el módulo 'utils'
# Si ya configuraste PYTHONPATH, esta línea no sería necesaria
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import create_video_capture, is_raspberry_pi

def capture_camera_image(output_path=None):
    """
    Captura una imagen desde la cámara y la guarda en un archivo.
    
    Si se está ejecutando en una Raspberry Pi se utiliza libcamera (el mismo stack
    que usa libcamera-still), de lo contrario se utiliza OpenCV.
    
    Si no se especifica output_path, se guarda en la carpeta 'vision' junto a este
    archivo, con el nombre 'captured_image.jpg'.
    
    :param output_path: Ruta donde se guardará la imagen.
    :return: Ruta del archivo de la imagen capturada o None si falla.
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
        
        # Tiempo de espera para que la cámara se estabilice
        time.sleep(2)
        
        # Intentar leer el frame en varios intentos
        max_attempts = 5
        attempts = 0
        ret = False
        frame = None
        while attempts < max_attempts and not ret:
            ret, frame = cap.read()
            if not ret:
                print(f"[DEBUG] Intento {attempts + 1} fallido, reintentando...")
                time.sleep(0.2)
            attempts += 1

        cap.release()

        if not ret or frame is None:
            print("Error: no se pudo capturar la imagen")
            return None

        cv2.imwrite(output_path, frame)
        print(f"📸 Imagen capturada (con OpenCV) guardada en {output_path}")
        return output_path

def analyze_image(image_path, model="gpt-4o-mini", max_tokens=300):
    """
    Envía una imagen a la API de OpenAI Vision para su análisis usando el endpoint
    de Chat Completions y la nueva interfaz de OpenAI.
    La imagen se codifica en Base64 y se envía como parte del mensaje.

    Si la variable de entorno OPENAI_API_KEY no está configurada se lanza un error.

    :param image_path: Ruta de la imagen a analizar.
    :param model: Modelo de OpenAI a utilizar para el análisis.
    :param max_tokens: Número máximo de tokens en la respuesta.
    :return: Respuesta del modelo en texto.
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("La variable de entorno OPENAI_API_KEY no está configurada")

    client = openai.OpenAI()
    
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "¿Qué ves en esta imagen?"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    image_path = capture_camera_image()
    if image_path:
        try:
            result = analyze_image(image_path)
            print("Análisis de la imagen:", result)
        except Exception as e:
            print("Error al analizar la imagen:", e)