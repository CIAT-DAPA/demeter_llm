
from src.domain.intent_classifier import classify_and_extract
from src.adapters.api_retriever import get_agroclimate_info
from src.adapters.generator import generate_response
from src.resources.geographic_data import GeographicData

def handle_user_input(user_input: str, user_id: str) -> dict:
    """
    Process user input text, extract information, query external data, and generate response.
    """
    request_data = classify_and_extract(user_input)
    print("Classify and extract")
    print(request_data)
    data = []
    if request_data.get("type") == "climate" or request_data.get("type") == "crop":
        data = get_agroclimate_info(request_data)
    elif request_data.get("type") == "location":
        if request_data.get("location") == None:
            data = GeographicData.get_instance().get_all_countries()
        else:
            data = GeographicData.get_instance().fuzzy_match_location_many(request_data.get("location"))
    #print("data")
    #print(data)
    response = generate_response(user_input, data, request_data)
    return {"user_id": user_id, "response": response}
    #return {"user_id": user_id, "response": "Hola"}
