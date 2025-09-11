from abc import abstractmethod

from Interfaces.IModelResponse import IResponse


class IModel:
    @abstractmethod
    def prompt(self, prompt: str) -> IResponse:
        pass
