import re

from flask import request
from passlib.handlers.sha2_crypt import sha256_crypt

from models import User
from requirement.PasswordFormatHandler import PasswordFormatHandler
from requirement.UsernameFormatHandler import UsernameFormatHandler
from routes.routeutil.SessionUtils import startSession
from util.GDate import GDate

usernameHandler = UsernameFormatHandler()
passwordHandler = PasswordFormatHandler()
usernameHandler.setNext(passwordHandler)

userRepo = User.objects


def loginHandler():
    jsonData = request.get_json()

    if jsonData["isEmail"]:
        jsonData["email"] = jsonData["username"]
        del jsonData["username"]
    else:
        result = usernameHandler.handle(jsonData)  # raise Exception atsin str dondurme exception tree yap
        if not result == "":
            return result

    identityUser = User(**jsonData)
    user = userRepo.filter(**{"$or": [{"email": re.compile(str(identityUser.email), re.IGNORECASE)},
                                      {"username": re.compile(str(identityUser.username), re.IGNORECASE)}]})
    if user:
        if sha256_crypt.verify(identityUser.password, user.password):
            startSession(user)
            userRepo.pushUpdate(user._id, **{'logged_on': GDate.getTimeWithFormat()})
            return None

    return "boyle bir kullanici adi veya email bulunamadi. Eminseniz sifrenizin dogrulugundan emin olun"
