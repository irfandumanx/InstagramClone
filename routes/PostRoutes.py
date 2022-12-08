from flask import Blueprint

from routes.postroutes.LikePost import likeActionHandler
from routes.postroutes.PostUpload import postUploadHandler
from routes.postroutes.ProfilePhoto import uploadProfilePhotoHandler, removeProfilePhotoHandler
from util import RouteRequirement

photoBlueprint = Blueprint("photoBlueprint", __name__)


@photoBlueprint.route("/photo/<photoID>/like-action", methods=["POST"])
@RouteRequirement.loginRequirement
def likeAction(photoID):
    return likeActionHandler(photoID)


@photoBlueprint.route("/uploadprofilephoto", methods=["POST"])
@RouteRequirement.loginRequirement
def uploadProfilePhoto():
    uploadProfilePhotoHandler()
    return "", 204


@photoBlueprint.route("/removeprofilephoto", methods=["POST"])
@RouteRequirement.loginRequirement
def removeProfilePhoto():
    return removeProfilePhotoHandler()


@photoBlueprint.route("/postupload", methods=["POST"])
@RouteRequirement.loginRequirement
def postUpload():
    postUploadHandler()
    return "", 204
