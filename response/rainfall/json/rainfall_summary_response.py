import json

from model.rainfall.rainfall_summary import RainfallSummary


class RainfallSummaryResponseJson(object):
    def __init__(self, model: RainfallSummary):
        self.model = model
    
    def get_response(self):
        return json.dumps({'rainfall_summaries': 
            self.model.__dict__}, ensure_ascii=False)