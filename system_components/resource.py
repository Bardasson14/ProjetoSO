from abc import ABC, abstractmethod

class Resource(ABC):

    @abstractmethod
    def __init__(self, avaliable):
        self.avaliable = avaliable
