# chat_manager.py
import os
import requests

def load_system_personality(file_path: str) -> str:
    """
    Lee el contenido del archivo 'personality_system.txt' (o el que se indique)
    para usarlo como 'rol system' de K-VRC.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def get_chat_response(user_text: str, personality_file="personality_system.txt") -> str:
    """
    Envía 'user_text' al endpoint de ChatGPT y devuelve la respuesta.
    Usa un rol 'system' leído de un archivo externo.
    """
    # Leemos la personalidad desde el archivo
    system_content = load_system_personality(personality_file)

    url = "https://api.openai.com/v1/chat/completions"
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("La variable OPENAI_API_KEY no está configurada en el entorno.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",  # o gpt-4, si lo tienes habilitado
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_text},
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }

    # Petición POST al endpoint de ChatGPT
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    result_json = response.json()
    return result_json["choices"][0]["message"]["content"].strip()
