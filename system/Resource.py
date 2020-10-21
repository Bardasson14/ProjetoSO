from abc import ABC, abstractmethod

class Resource(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, status):
        self.status = status