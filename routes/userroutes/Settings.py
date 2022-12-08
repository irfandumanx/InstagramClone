from random import Random

from flask import request, session

from managers.MailManager import MailManager
from models import User
from requirement.EmailFormatHandler import EmailFormatHandler
from requirement.NameFormatHandler import NameFormatHandler
from requirement.SameUsernameHandler import SameUsernameHandler
from requirement.UsernameFormatHandler import UsernameFormatHandler
from routes.routeutil.SessionUtils import startSession

mailHandler = EmailFormatHandler()
nameHandler = NameFormatHandler()
usernameHandler = UsernameFormatHandler()
sameUsernameHandler = SameUsernameHandler()
usernameHandler.setNext(sameUsernameHandler)

mailManager = MailManager()
random = Random()
userRepo = User.objects


def settingsHandle():
    changed = False
    user = User(**session["user"])
    dbUser = userRepo.filter(**{"_id": user._id})
    requestForm = request.form
    updateDict = dict()

    if not dbUser.name == requestForm.get("name"):
        errorMessage = nameHandler.handle(requestForm)
        if errorMessage:
            return errorMessage
        updateDict["name"] = requestForm.get("name")
        changed = True

    if not dbUser.username == requestForm.get("username"):
        errorMessage = usernameHandler.handle(requestForm)
        if errorMessage:
            return errorMessage
        updateDict["username"] = requestForm.get("username")
        changed = True

    if changed:
        userRepo.setUpdate(dbUser._id, **updateDict)
        user.name = requestForm.get("name")
        user.username = requestForm.get("username")
        startSession(user)

    if not dbUser.email == request.form.get("email"):
        code = str(random.randint(100000, 999999))
        userRepo.setUpdate(dbUser._id, **{"email_validation": code})
        session["excepted_mail"] = request.form.get("email")
        mailManager.sendMailValidation(dbUser.email, code)
        return "Mail Gonderildi"


def mailValidation() -> bool:
    user = User(**session["user"])
    code = request.args.get("code")
    dbUser = userRepo.filter(**{"_id": user._id})
    if dbUser.mailValidationCode == code:
        user.email = session["excepted_mail"]
        userRepo.setUpdate(user._id, **{"email": session["excepted_mail"], "email_validation": "0"})
        startSession(user)
        return True

    return False
