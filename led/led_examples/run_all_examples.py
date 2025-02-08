import os
import sys
import glob
import importlib.util
import time

print("Current directory:", os.getcwd())
print("Script location:", os.path.dirname(__file__))

# Se calcula el directorio raíz del proyecto (dos niveles arriba)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
print("Project root path:", project_root)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

def run_example(script_path):
    script_name = os.path.basename(script_path)
    # Evitar ejecutar este mismo script
    if script_name == "run_all_examples.py":
        return
    
    print("\n" + "="*50)
    print(f"Ejecutando: {script_name}")
    print("="*50)
    
    try:
        # Importar y ejecutar el script
        spec = importlib.util.spec_from_file_location("example", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Si el script define una función main(), se ejecuta
        if hasattr(module, "main"):
            module.main()
        
        print(f"\nEjemplo {script_name} completado.")
        time.sleep(2)  # Pequeña pausa entre ejemplos
        
    except KeyboardInterrupt:
        print(f"\nEjemplo {script_name} interrumpido por el usuario.")
    except Exception as e:
        print(f"\nError al ejecutar {script_name}: {e}")
    
    print("-"*50 + "\n")

def main():
    # Buscar todos los scripts .py en la carpeta led_examples
    examples_dir = os.path.dirname(os.path.abspath(__file__))
    example_scripts = glob.glob(os.path.join(examples_dir, "*.py"))
    
    # Contar los ejemplos, excluyendo este script
    num_scripts = len([s for s in example_scripts if os.path.basename(s) != "run_all_examples.py"])
    print(f"Encontrados {num_scripts} ejemplos para ejecutar.\n")
    
    # Ejecutar cada ejemplo en orden alfabético
    for script_path in sorted(example_scripts):
        run_example(script_path)

if __name__ == "__main__":
    try:
        main()
        print("\nTodos los ejemplos han sido ejecutados.")
    except KeyboardInterrupt:
        print("\nEjecución interrumpida por el usuario.")
    except Exception as e:
        print(f"\nError durante la ejecución: {e}") 