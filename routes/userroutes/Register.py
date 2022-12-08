import re

from flask import request
from passlib.handlers.sha2_crypt import sha256_crypt
from models.User import User
from requirement import EmailFormatHandler, NameFormatHandler, UsernameFormatHandler, PasswordFormatHandler
from routes.routeutil.SessionUtils import startSession
from util.GDate import GDate

mailHandler = EmailFormatHandler.EmailFormatHandler()
nameHandler = NameFormatHandler.NameFormatHandler()
usernameHandler = UsernameFormatHandler.UsernameFormatHandler()
passwordHandler = PasswordFormatHandler.PasswordFormatHandler()
mailHandler.setNext(nameHandler).setNext(usernameHandler).setNext(passwordHandler)

userRepo = User.objects


def registerHandler():
    jsonData = request.get_json()

    result = mailHandler.handle(jsonData)  # raise Exception atsin str dondurme exception tree yap
    if not result == "":
        return result

    user = User(**jsonData)

    user.password = sha256_crypt.hash(user.password)
    user.createdOn = GDate.getTimeWithFormat()

    if userRepo.filter(**{"email": re.compile(user.email, re.IGNORECASE)}):
        return "Bu mail kullaniliyor"
    elif userRepo.filter(**{"username": re.compile(user.username, re.IGNORECASE)}):
        return "Bu kullanici adi kullaniliyor"

    if userRepo.insert(**user.serialize(idOnly=False)) is None:  # insert user to db
        return "Kayit esnasinda bir hata meydana geldi"

    startSession(user)
    return None
