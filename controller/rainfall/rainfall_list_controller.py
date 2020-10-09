from services.rainfall.rainfall_list_service import RainfallListService


class RainfallListController(object):
    def __init__(self, service):
        self.service = service

    def get(self):
        rainfall_list = self.service.get_list()
        response = []
        for rainfall in rainfall_list:
            response.append(rainfall.json())
        
        return response