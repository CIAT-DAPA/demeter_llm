
from src.domain.intent_classifier import classify_and_extract
from src.adapters.api_retriever import get_agroclimate_info
from src.adapters.generator import generate_response

def handle_user_input(user_input: str, user_id: str) -> dict:
    """
    Process user input text, extract information, query external data, and generate response.
    """
    request_data = classify_and_extract(user_input)
    data = get_agroclimate_info(request_data)
    #print("data")
    #print(data)
    response = generate_response(user_input, data, request_data)
    return {"user_id": user_id, "response": response}
