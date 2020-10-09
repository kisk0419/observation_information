import abc


class RainfallRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def find_all(self, unit, area_no):
        pass