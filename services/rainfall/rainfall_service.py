import abc


class RainfallService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, unit):
        pass