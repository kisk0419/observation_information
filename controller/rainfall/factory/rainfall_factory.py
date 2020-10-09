from controller.rainfall.rainfall_controller import RainfallController
from services.rainfall.scraping.rainfall_service import RainfallService as ScrapingRainfallService

class RainfallFactory(object):
    def __init__(self, mode):
        self.mode = mode

    def create_controller(self):
        if self.mode == 'scraping':
            controller = RainfallController(ScrapingRainfallService())
            return controller
        raise Exception()