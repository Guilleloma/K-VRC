import os
import json
import requests
from collections import deque

# Nueva ruta dentro de la carpeta chat/
CHAT_MEMORY_DIR = "chat"
MEMORY_FILE = os.path.join(CHAT_MEMORY_DIR, "chat_memory.json")
MAX_MEMORY = 80  # Número máximo de interacciones a recordar

# Asegurar que la carpeta chat existe
if not os.path.exists(CHAT_MEMORY_DIR):
    os.makedirs(CHAT_MEMORY_DIR)

# Cargamos la memoria desde el archivo JSON (si existe)
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return deque(json.load(f), maxlen=MAX_MEMORY)
    return deque(maxlen=MAX_MEMORY)

# Guardamos la memoria en el archivo JSON
def save_memory(history):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(list(history), f, indent=4)

# Inicializamos la memoria
chat_history = load_memory()

def load_system_personality(file_path: str) -> str:
    """Carga la personalidad del sistema desde un archivo de texto."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def get_chat_response(user_text: str, personality_file="chat/personality_system.txt") -> str:
    """Envía 'user_text' a la API de OpenAI con memoria guardada en JSON."""
    system_content = load_system_personality(personality_file)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("La variable OPENAI_API_KEY no está configurada en el entorno.")

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    messages = [{"role": "system", "content": system_content}] + list(chat_history)
    messages.append({"role": "user", "content": user_text})

    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 150
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    result_json = response.json()
    chat_response = result_json["choices"][0]["message"]["content"].strip()

    # Guardamos la conversación en memoria y en JSON
    chat_history.append({"role": "user", "content": user_text})
    chat_history.append({"role": "assistant", "content": chat_response})
    save_memory(chat_history)

    return chat_response
