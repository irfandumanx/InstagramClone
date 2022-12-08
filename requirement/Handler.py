from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class Handler(ABC): #chain of responsibility

    @abstractmethod
    def setNext(self, handler: Handler) -> Handler: #builder pattern
        raise NotImplementedError

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        raise NotImplementedError
