from flask import Blueprint, render_template, redirect, session

from models import User
from routes.userroutes.Login import loginHandler
from routes.userroutes.Logout import logoutHandler
from routes.userroutes.Register import registerHandler
from routes.userroutes.Settings import settingsHandle, mailValidation
from util import RouteRequirement
from util.GImage import GImage

userBlueprint = Blueprint("userBlueprint", __name__)
uploadProfilePhotoBlueprint = Blueprint("uploadProfilePhotoBlueprint", __name__)
postUploadBlueprint = Blueprint("postUploadBlueprint", __name__)

jsonData = {'errorMessage': None, 'url': "http://127.0.0.1:8080"}


@userBlueprint.route("/register", methods=["POST"])
def postRegister():
    jsonData["errorMessage"] = registerHandler()
    return __checkError()


@userBlueprint.route("/register", methods=["GET"])
def getRegister():
    return render_template("register.html")


@userBlueprint.route("/login", methods=["POST"])
def postLogin():
    jsonData["errorMessage"] = loginHandler()
    return __checkError()


@userBlueprint.route("/login", methods=["GET"])
def getLogin():
    if "user" in session:
        return redirect("http://127.0.0.1:8080")
    return render_template("login.html")


@userBlueprint.route("/settings")
@RouteRequirement.loginRequirement
def getSettings():
    userIdentity = User(**session["user"])
    return render_template("settings.html", user=userIdentity,
                           image=GImage.decodeBase64FromPathWithExtension(userIdentity.profileImage))


@userBlueprint.route("/mail-validation")
@RouteRequirement.loginRequirement
def getMailValidation():
    userIdentity = User(**session["user"])
    isValidate = mailValidation()
    return render_template("mail.html", isValidate=isValidate, user=userIdentity,
                           image=GImage.decodeBase64FromPathWithExtension(userIdentity.profileImage))


@userBlueprint.route("/update-profile", methods=["POST"])
@RouteRequirement.loginRequirement
def postSettings():
    jsonData["errorMessage"] = settingsHandle()
    return __checkError()


@userBlueprint.route("/logout")
def logout():
    logoutHandler()
    return redirect("http://127.0.0.1:8080")  # env kullan


def __checkError():
    if jsonData["errorMessage"] is None:
        jsonData["url"] = "http://127.0.0.1:8080"
    else:
        jsonData["url"] = None

    return jsonData
