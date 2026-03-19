from abc import ABC, abstractmethod

class InterfaceSaleItem(ABC):

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def remove(self):
        pass 

    @abstractmethod
    def monthly_profit(self):
        pass