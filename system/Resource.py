from abc import ABC, abstractmethod

class Resource(ABC):

    @abstractmethod
    def __init__(self, status):
        self.status = status
