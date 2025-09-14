from abc import abstractmethod

from Interfaces.IModelResponse import IModelResponse


class IModel:
    first_prompt: str | None = None

    def __init__(self, initial: str | None = None):
        if initial is not None:
            first_prompt = initial

    @abstractmethod
    def prompt(self, prompt: str) -> IModelResponse:
        pass
