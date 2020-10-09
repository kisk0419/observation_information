import abc


class RainfallListRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def find_all(self, area_no):
        pass