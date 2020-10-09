from controller.rainfall.factory.rainfall_list_factory import RainfallListFactory
from controller.rainfall.factory.rainfall_factory import RainfallFactory


if __name__ == '__main__':
    factory = RainfallListFactory('scraping')
    c = factory.create_controller()
    print(c.get())

    factory = RainfallFactory('scraping')
    c = factory.create_controller()
    print(c.get())
    