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
        You are an expert agroclimate assistant.
        You have to identify the type of user who is asking for information.
        You have to identify the type of request from the user, it could be for climate, crops, locations, help or others.
        When the request is about climate you should define if the request was about historical, climatology or forecast;
            the difference between historical and climatology is when user specific the year, in this case is historical otherwise is climatology.
        When the request is about crop you should define which crops or cultivars are in.
        All dates should be reporte in the following JSON format: year:YYYY, month:MM, day:dd, fill with "0" the items that you don't identify in the same format.
        Extract:
        - type_user: "producer" or "extension agent" or "decision maker" or "scientist" or "general public"
        - type: "climate" or "crop" or "location" or "help" or "others"
        - time: "historical" or "climatology" or "forecast"
        - time_value: any date mentioned
        - location: any place mentioned
        - variable: if type is climate e.g., "precipitation", "temperature", "humidity"; otherwise return crop or cultivar e.g., "rice", "maize"
        Question: "{text}"
        If not found, use null. Use JSON format. Return JSON Only
    """
    print(prompt)
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
