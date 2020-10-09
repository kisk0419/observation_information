import abc


class RainfallListService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_list(self):
        pass