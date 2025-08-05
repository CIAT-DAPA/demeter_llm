"""
Singleton class to cache Aclimate geographic locations and allow fuzzy location lookup.
"""
import pandas as pd
from aclimate_api.agronomy import Agronomy
from src.config import config
import threading

class AgronomyData:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        if AgronomyData._instance is not None:
            raise Exception("This class is a singleton!")
        self.aclimate = Agronomy(config["ACLIMATE_API_BASE_URL"])
        self.setup_data = []
        self._load_all_setups()
        AgronomyData._instance = self

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = AgronomyData()
            return cls._instance

    def _load_all_setups(self):
        #print("listar setups")
        all_setups = self.aclimate.get_agronomy()
        #print(all_setups)
        self.setup_data = all_setups

    def get_all_setups(self):
        return self.setup_data

