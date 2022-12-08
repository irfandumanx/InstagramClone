from requirement.AbstractHandler import AbstractHandler
from typing import Any


class NameFormatHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        name = request["name"]
        if name == "" or name is None:
            return "Isim bos birakilamaz"
        else:
            return super().handle(request)
