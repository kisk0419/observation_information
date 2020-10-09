from controller.rainfall.rainfall_list_controller import RainfallListController
from services.rainfall.scraping.rainfall_list_service import RainfallListService as ScrapingRainfallListService

class RainfallListFactory(object):
    def __init__(self, mode):
        self.mode = mode

    def create_controller(self):
        if self.mode == 'scraping':
            controller = RainfallListController(ScrapingRainfallListService())
            return controller
        raise Exception()