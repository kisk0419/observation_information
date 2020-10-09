from services.rainfall.rainfall_service import RainfallService


class RainfallController(object):
    def __init__(self, service):
        self.service = service

    def get(self, unit=10):
        rainfalls = self.service.get(unit)
        response = []
        for rainfall in rainfalls:
            response.append(rainfall.json())
        
        return response