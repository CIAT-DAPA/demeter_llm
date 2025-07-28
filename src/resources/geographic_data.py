"""
Singleton class to cache Aclimate geographic locations and allow fuzzy location lookup.
"""
import pandas as pd
from aclimate_api.geographic import Geographic
from src.config import config
from difflib import get_close_matches
import threading

class GeographicData:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        if GeographicData._instance is not None:
            raise Exception("This class is a singleton!")
        self.aclimate = Geographic(config["ACLIMATE_API_BASE_URL"])
        self.geo_data = []
        self._load_all_locations()
        GeographicData._instance = self

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = GeographicData()
            return cls._instance

    def _load_all_locations(self):
        #print("listar paises")
        countries = self.aclimate.get_geographic_country()
        #print(countries)
        all_sites = None
        for index,country in countries.iterrows():
            #print("Country: " + country["id"])
            try:
                if all_sites is None:
                    all_sites = self.aclimate.get_geographic(country["id"])
                else:
                    all_sites = pd.concat([all_sites, self.aclimate.get_geographic(country["id"])], ignore_index=True)
                    #all_sites = all_sites.append(self.aclimate.get_geographic(country["id"]), ignore_index=True)
            except Exception as e:
                print(f"Failed to load sites for {country['id']}: {e}")
        #print(all_sites)
        self.geo_data = all_sites

    def get_all_locations(self):
        return self.geo_data

    def fuzzy_match_location(self, user_location: str) -> dict:
        #print("buscando sitio")
        names = self.geo_data["ws_name"].to_list()
        #print(names)
        #print("Matches " + user_location)
        matches = get_close_matches(user_location, names, n=1, cutoff=0.6)
        #print(matches)
        if matches:
            for index,site in self.geo_data.iterrows():
                #print(site)
                if site["ws_name"] == matches[0]:
                    return site
        return None
