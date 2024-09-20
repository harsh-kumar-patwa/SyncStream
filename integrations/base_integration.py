from abc import ABC, abstractmethod

class Integration(ABC):
    @abstractmethod
    def create_customer(self,name,email):
        pass

    @abstractmethod
    def update_customer(self,external_id,**kwargs):
        pass

    @abstractmethod
    def delete_customer(self, external_id):
        pass