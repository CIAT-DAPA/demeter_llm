import requests
import json
from src.config import config


def classify_and_extract(text: str) -> dict:
    """
    Uses Ollama API to classify and extract domain-specific information.

    Args:
        text (str): Natural language question

    Returns:
        dict: A JSON with keys: type, time, location, variable
    """
    prompt = f"""
        You are an expert agroclimate assistant. Yo have to identify the type of user who is asking for agroclimatic information. 
        Extract:
        - type_user: "producer" or "extension agent" or "decision maker" or "scientist" or "other"
        - type: "climate" or "crop" or "location"
        - time: "historical" or "forecast"
        - location: any place mentioned
        - variable: if type is climate e.g., "precipitation", "temperature", "humidity"; otherwise return crop or cultivar e.g., "rice", "maize"
        Question: "{text}"
        If not found, use null. Use JSON format. Return JSON Only
    """
    response = requests.post(config['OLLAMA_API_URL'], json={
        "model": config['OLLAMA_MODEL'],
        "prompt": prompt,
        "stream": False
    })

    #print(response.json())
    try:
        raw_output = response.json()["response"]
        start = raw_output.find("{")
        end = raw_output.rfind("}") + 1
        #print(raw_output[start:end])
        return json.loads(raw_output[start:end])
    except Exception:
        return {}
