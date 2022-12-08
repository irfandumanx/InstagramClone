from flask import session
from models import User


def startSession(user: User):
    logout()
    session["user"] = {"_id": user._id, "email": user.email, "username": user.username,
                       "name": user.name, "created_on": user.createdOn,
                       "profile_image_path": user.profileImage}


def logout():
    session.clear()
