from requirement.AbstractHandler import AbstractHandler
from typing import Any


class PasswordFormatHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        password = request["password"]
        if password == "" or password is None:
            return "Sifre bos birakilamaz"
        else:
            return super().handle(request)
