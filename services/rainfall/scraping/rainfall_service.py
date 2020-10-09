from services.rainfall.rainfall_service import RainfallService as BaseService
from repository.scraping.rainfall_repository import RainfallRepository


class RainfallService(BaseService):
    def __init__(self):
        self.repository = RainfallRepository()

    def get(self, unit=10):
        rainfalls = self.repository.find_all(unit)
        return rainfalls
