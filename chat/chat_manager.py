# chat_manager.py 
import os
import requests

def get_chat_response(user_text: str) -> str:
    """
    Envía 'user_text' al endpoint de ChatGPT (/v1/chat/completions)
    y devuelve la respuesta como string.
    """
    url = "https://api.openai.com/v1/chat/completions"
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("La variable OPENAI_API_KEY no está configurada en el entorno.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Arma los mensajes: un "system" para dar contexto/rol a K-VRC, y el "user" con el texto
    data = {
        "model": "gpt-3.5-turbo",  # O 'gpt-4' si lo tienes habilitado
        "messages": [
            {"role": "system", "content": "Eres K-VRC, un simpático robot de Love, Death & Robots. Estás programado para ayudar."},
            {"role": "user", "content": user_text},
        ],
        "temperature": 0.7,
        "max_tokens": 150,
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    # La respuesta es un JSON con 'choices'
    result_json = response.json()
    return result_json["choices"][0]["message"]["content"].strip()
