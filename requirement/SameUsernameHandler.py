from models import User
from requirement.AbstractHandler import AbstractHandler
from typing import Any

userRepo = User.objects


class SameUsernameHandler(AbstractHandler):

    def handle(self, request: Any) -> str:
        if "username" in request:
            if userRepo.filter(**{"username": request["username"]}):
                return "Bu kullanici adi kullanilmakta"

        return super().handle(request)
