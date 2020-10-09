import json

from model.base_model import BaseModel

"""
雨量集計情報
"""
class RainfallSummary(BaseModel):
    def __init__(self, observation_name: str):
        self.observation_name = observation_name
        self.amount_10m = ''
        self.amount_60m = ''
        self.amount_1h = ''
        self.amount_3h = ''
        self.amount_6h = ''
        self.amount_24h = ''
        self.amount_total = ''
        self.start_time = ''
        self.office_name = ''
        self.city_name = '' 
