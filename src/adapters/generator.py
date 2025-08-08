import requests
#import json
import pandas as pd
from pandas import DataFrame
from src.resources.geographic_data import GeographicData
from src.config import config

def generate_response(user_input: str, data: dict, request_data: dict) -> str:
    type_request = request_data.get("type")
    user_type = request_data.get("type_user")
    data_summary = {}
    if type_request == "climate" or type_request == "crop":
        data_summary = summarize_data(data)
    elif type_request == "location":
        data_summary = data["name"].to_json()

    #print("datos")
    print(data.columns)
    #print("datos 2")
    #print(data_summary)

    prompt = "Your name is Melisa chatbot."
    if type_request == "climate":
        prompt = prompt + f"""
        You are the best climatologist assistant for a {user_type}.
        You have to answer the user request.
        If user didn't declare the variable, you have to summarize all variables.
        You have to take into account the Type request to generate the answer
            * historical:
                - Always give a summary for the years requested
            * forecast:
                - Always the data that you provided are probabilities about excess of rainfall, the categories are: above normal, below normal and normal.
                - The month in the data is the center of the quarter
            * climatology
                - Say it is climatology
        User: "{user_input}"
        Instructions:
        - You have to filter data by measure, in this case use the context Variable.
        - You have to filter data by year and/or month, in this case use the context Time.
        - Never recommend to search in other places or develop an script.
        - Respond clearly and use vocabulary appropriate for the user type and the same language.
        Context:
        - Time: {request_data.get('time_value')}
        - Variable: {request_data.get('variable')}
        - Type request: {request_data.get('time')} 
        Data: {data_summary}
    """
    elif type_request == "crop":
        #with open("./archivo.txt", "w", encoding="utf-8") as f:
        #    f.write(data_summary)
        prompt = prompt + f"""
        You are the best agroclimatic assistant for a {user_type}.
        You always have to answer the user request.
        Do not give recommendations on how to process the data, especially don't give source code.
        You recevie Data, that is a list of dictionaries in JSON format, containing various metrics related to crop growth and weather conditions. Here's a breakdown of the data:
        Configuration:
        1. cultivar: The type of crop cultivar being measured
        2. soil: The type of soil
        3. crop_name: The name of the crop
        4. start and end: Dates representing the start and end dates of the optimal planting date.
        Metrics:
        1. measure: The type of measurement (e.g., yield_14, yield_0, etc.)
        2. median, avg, min, max: Statistical values for each metric
        3. quar_1, quar_2, quar_3: Quantiles (25th, 50th, and 75th percentiles) for each metric
        4. conf_lower and conf_upper: Lower and upper bounds of the confidence interval for each metric
        5. sd: Standard deviation for each metric
        6. perc_5 and perc_95: 5th and 95th percentiles for each metric
        7. coef_var: Coefficient of variation (standard deviation divided by the mean) for each metric
        Instructions:
        * Identify the best configuration - select the combination of crop,
            cultivar, soil, and planting period (start, end) that produces the highest average value.
        * Generate a detailed report including:
            - A clear description of the best configuration (names + planting dates).
            - The highest average yield found, with a brief note on statistical reliability (e.g. confidence interval and percentiles).
        * Always indicates the yield of the crop and say that it is potential yield.
        * Yield is always kg/ha.
        * Dates should be given in format readable.
        * Never recommend to search in other places.
        * Respond clearly and use vocabulary appropriate for the user type and the same language.
        * Ensure your recommendations are concise, actionable, and based on the agroclimatic indicators of the chosen configuration.
            Use domain-appropriate language (agriculture + climate) to communicate clearly with {user_type}.
        User: "{user_input}"
        Data: {data_summary}
    """
    elif type_request == "location":
        prompt = prompt + f"""
        You are the best agroclimate assistant for a {user_type}.
        You have to answer the user request.
        You have to generate an understandable list of available locations using Data so that the user can say what they are looking for.
        Don't show code to filter the list.
        User: "{user_input}"
        Instructions:
        - Sort the list alphabetically.
        - Never recommend to search in other places.
        - Respond clearly and use vocabulary appropriate for the user type and the same language.
        Data: {data_summary}
    """
    else:
        prompt = prompt + f"""
        You are the best agroclimate assistant.
        You have to answer the user request.
        User: "{user_input}"
        Instructions:
        - If user greet, greet.
        - If user ask about your origin, tell them the tale about Greek godness Demeter and the Melisas.
        - If user request for help or manual user say: OK.
        - Never recommend to search in other places.
        - Respond clearly and use vocabulary appropriate for the user type and the same language.
    """

    try:
        print(prompt)
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