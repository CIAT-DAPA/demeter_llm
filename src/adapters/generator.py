import requests
import json

OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"

def generate_response(user_input: str, data: dict, context: dict) -> str:
    user_type = infer_user_type(user_input)
    data_summary = summarize_data(data)

    prompt = f"""
You are an agroclimate assistant for a {user_type}.
User: "{user_input}"
Context:
- Type: {context.get('type')}
- Time: {context.get('time')}
- Location: {context.get('location')}
- Variable: {context.get('variable')}
Data: {data_summary}
Respond clearly and use vocabulary appropriate for the user type.
"""

    try:
        response = requests.post(OLLAMA_API_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        })
        return response.json()["response"].strip()
    except:
        return "Error al generar respuesta."

def summarize_data(data: dict) -> str:
    try:
        return json.dumps(data, indent=2, ensure_ascii=False)
    except:
        return "No se pudieron resumir los datos."

def infer_user_type(text: str) -> str:
    text = text.lower()
    if "política" in text or "gobierno" in text:
        return "tomador de decision"
    elif "asistencia técnica" in text or "productores" in text:
        return "extensionista"
    return "agricultor"
