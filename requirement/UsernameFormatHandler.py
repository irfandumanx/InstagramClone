from requirement.AbstractHandler import AbstractHandler
from typing import Any


class UsernameFormatHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        username = request["username"]
        if username == "" or username is None:
            return "Kullanici adi bos birakilamaz"
        else:
            return super().handle(request)
