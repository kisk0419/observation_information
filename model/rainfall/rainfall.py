import json

from .base_model import BaseModel


class Rainfall(BaseModel):
    def __init__(self, unit: str, observation_name: str):
        self.unit = unit
        self.observation_name = observation_name
        self.start_time = ''
        self.timelines = []

    def json(self):
        timelines = [timeline.__dict__ for timeline in self.timelines]
        return json.dumps({'unit': self.unit, 'observation_name': self.observation_name,
                           'start_time': self.start_time, 'timelines': timelines}, ensure_ascii=False)
        

class RainfallTimeLine(BaseModel):
    def __init__(self, datetime: str):
        self.datetime = datetime
        self.unit_amount = ''
        self.total_amount = ''
      
    def json(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

