from requirement.Handler import Handler
from abc import abstractmethod
from typing import Any


class AbstractHandler(Handler):
    nextHandler: Handler = None

    def setNext(self, handler: Handler) -> Handler:
        self.nextHandler = handler
        return handler

    @abstractmethod
    def handle(self, request: Any) -> str:
        if self.nextHandler:
            return self.nextHandler.handle(request)

        return ""
