import requests
#import json
import pandas as pd
from pandas import DataFrame
from src.config import config

def generate_response(user_input: str, data: dict, request_data: dict) -> str:
    print("user")
    user_type = request_data.get("type_user")
    print(user_type)
    data_summary = summarize_data(data)
    #print("datos")
    #print(data_summary)
    prompt = f"""
        You are an agroclimate assistant for a {user_type}.
        User: "{user_input}"
        Context:
        - Type: {request_data.get('type')}
        - Time: {request_data.get('time')}
        - Location: {request_data.get('location')}
        - Variable: {request_data.get('variable')}
        Data: {data_summary}
        Respond clearly and use vocabulary appropriate for the user type. Never recommend to search in other places.
    """

    try:
        print()
        response = requests.post(config['OLLAMA_API_URL'], json={
            "model": config['OLLAMA_MODEL'],
            "prompt": prompt,
            "stream": False
        })
        print("respuesta")
        print(response.json()["response"].strip())
        return response.json()["response"].strip()
    except:
        return "Error al generar respuesta."

def summarize_data(data: DataFrame) -> str:
    try:
        #return json.dumps(data, indent=2, ensure_ascii=False)
        return data.to_json(orient="records")
    except:
        return "No se pudieron resumir los datos."