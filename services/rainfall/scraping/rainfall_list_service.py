from services.rainfall.rainfall_list_service import RainfallListService as BaseService
from repository.scraping.rainfall_list_repository import RainfallListRepository


class RainfallListService(BaseService):
    def __init__(self):
        self.repository = RainfallListRepository()

    def get_list(self):
        rainfall_list = self.repository.find_all()
        return rainfall_list
