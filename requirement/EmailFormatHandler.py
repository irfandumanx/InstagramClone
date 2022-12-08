from requirement.AbstractHandler import AbstractHandler
from typing import Any
import re


class EmailFormatHandler(AbstractHandler):
    EMAIL_REGEX = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    def handle(self, request: Any) -> str:
        if "email" in request:
            if not re.search(self.EMAIL_REGEX, request["email"]):
                return "Lutfen gecerli bir mail formati giriniz"

        return super().handle(request)
