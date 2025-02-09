#!/usr/bin/env python3
import os
import glob
import sys
import subprocess

def run_example(example_path):
    print("=" * 50)
    print(f"Ejecutando ejemplo: {example_path}")
    print("=" * 50)
    # Utiliza el intérprete actual (sys.executable) para mayor robustez
    result = subprocess.run([sys.executable, example_path])
    if result.returncode != 0:
        print(f"Error: El ejemplo {example_path} falló con código {result.returncode}.")
    else:
        print(f"Ejemplo {example_path} ejecutado correctamente.")
    print("=" * 50 + "\n")

def test_camera():
    print("=" * 50)
    print("Ejecutando prueba del módulo de Cámara:")
    print("=" * 50)
    try:
        from vision.camera import capture_camera_image
        # Se llama a la función para capturar la imagen (no se requiere analizarla)
        image_path = capture_camera_image()
        if image_path and os.path.exists(image_path):
            print(f"Imagen capturada exitosamente: {image_path}")
        else:
            print("Error: No se pudo capturar la imagen con la cámara.")
    except Exception as e:
        print("Excepción durante la prueba de la cámara:", e)
    print("=" * 50 + "\n")

def main():
    # Se asume que la raíz del proyecto es el directorio donde se encuentra este script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Buscar de forma recursiva todos los archivos "run_all_examples.py" en el proyecto
    pattern = os.path.join(base_dir, "**", "run_all_examples.py")
    example_files = glob.glob(pattern, recursive=True)
    example_files.sort()

    if not example_files:
        print("No se encontraron archivos run_all_examples.py en el proyecto.")
    else:
        print("Se encontraron los siguientes archivos de ejemplos:")
        for f in example_files:
            print(" -", f)
        input("\nPresiona Enter para ejecutar todos los ejemplos secuencialmente...")

        for example in example_files:
            run_example(example)
            input("Presiona Enter para continuar con el siguiente ejemplo...")

    # Ejecutar la prueba del módulo de cámara
    input("Presiona Enter para ejecutar la prueba del módulo de Cámara...")
    test_camera()

if __name__ == "__main__":
    main() 