from aclimate_api.agronomy import Agronomy
from aclimate_api.historical import Historical
from aclimate_api.forecast import Forecast
from src.config import config
from src.resources.geographic_data import GeographicData
import datetime

def get_agroclimate_info(request_data: dict) -> dict:
    print("datos enviados")
    print(request_data)
    type_request = request_data.get("type")
    raw_location = request_data.get("location")
    variable = request_data.get("variable")
    time = request_data.get("time")

    geo_cache = GeographicData.get_instance()
    location = geo_cache.fuzzy_match_location(raw_location)
    #print("location")
    #print(location)
    locations_ids = [location["ws_id"]]
    try:
        if type_request == "climate":
            if time == "historical":
                historical = Historical(config["ACLIMATE_API_BASE_URL"])
                end = datetime.date.today()
                start = end - datetime.timedelta(days=30)
                return historical.get_historical_climatology(locations_ids)
            elif time == "forecast":
                forecast = Forecast(config["ACLIMATE_API_BASE_URL"])
                return forecast.get_forecast_climate(locations_ids)
        elif type_request == "crop":
            forecast = Forecast(config["ACLIMATE_API_BASE_URL"])
            return forecast.get_forecast_crop(locations_ids)
        return {"error": "Tiempo no reconocido"}
    except Exception as e:
        return {"error": str(e)}
