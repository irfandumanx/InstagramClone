import os

from flask import session, request
from werkzeug.utils import secure_filename, redirect

from models import User
from routes.routeutil.SessionUtils import startSession
from routes.routeutil.FileUtils import photoAllowedFile
from util.GImage import GImage

UPLOAD_FOLDER = "storage/photos"

userRepo = User.objects


def uploadProfilePhotoHandler():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if not (photoAllowedFile(file.filename)):
        return redirect(request.url)
    user = User(**session["user"])
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    userRepo.setUpdate(user._id, **{"profile_image_path": filename})
    user.profileImage = filename
    startSession(user)


def removeProfilePhotoHandler():
    user = User(**session["user"])
    userRepo.setUpdate(user._id, **{"profile_image_path": "img_avatar.png"})
    user.profileImage = "img_avatar.png"
    startSession(user)
    return GImage.decodeBase64FromPath("img_avatar.png")
