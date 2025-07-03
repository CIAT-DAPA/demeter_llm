from aclimate_api.agronomy import Agronomy
from aclimate_api.geographic import Geographic
from aclimate_api.historical import Historical
from aclimate_api.forecast import Forecast
from src.config import config
import datetime

def get_agroclimate_info(request_data: dict) -> dict:
    location = request_data.get("location")
    variable = request_data.get("variable")
    time = request_data.get("time")
    try:
        if time == "historico":
            historical = Historical(base_url=config["ACLIMATE_API_BASE_URL"])
            end = datetime.date.today()
            start = end - datetime.timedelta(days=30)
            return historical.get_historical_weather(location_name=location,
                                                   start_date=start.isoformat(),
                                                   end_date=end.isoformat(),
                                                   variables=[variable])
        elif time == "pronostico":
            forecast = Forecast(base_url=config["ACLIMATE_API_BASE_URL"])
            return forecast.get_forecast(location_name=location, variables=[variable])
        return {"error": "Tiempo no reconocido"}
    except Exception as e:
        return {"error": str(e)}
