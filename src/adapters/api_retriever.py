from aclimate_api.agronomy import Agronomy
from aclimate_api.historical import Historical
from aclimate_api.forecast import Forecast
from src.config import config
from src.resources.geographic_data import GeographicData
import datetime

def get_agroclimate_info(request_data: dict) -> dict:
    type_request = request_data.get("type")
    raw_location = request_data.get("location")
    time = request_data.get("time")
    time_value = request_data.get("time_value")
    geo_cache = GeographicData.get_instance()
    location = geo_cache.fuzzy_match_location(raw_location)
    #print("location")
    #print(location)
    locations_ids = [location["ws_id"]]
    try:
        if type_request == "climate":
            if time == "historical":
                historical = Historical(config["ACLIMATE_API_BASE_URL"])
                d = historical.get_historical_historicalclimatic(locations_ids)
                print("valor")
                print(time_value["year"])
                if "year" in time_value and (time_value["year"] != "0000" and time_value["year"] != "0"):
                    d = d[d["year"] == time_value["year"]]
                return d
            elif time == "forecast":
                forecast = Forecast(config["ACLIMATE_API_BASE_URL"])
                d = forecast.get_forecast_climate(locations_ids)
                return d['probabilities']
            else:
                historical = Historical(config["ACLIMATE_API_BASE_URL"])
                return historical.get_historical_climatology(locations_ids)
        elif type_request == "crop":
            forecast = Forecast(config["ACLIMATE_API_BASE_URL"])
            return forecast.get_forecast_crop(locations_ids)
        elif type_request == "location":
            return location
    except Exception as e:
        return {"error": str(e)}
