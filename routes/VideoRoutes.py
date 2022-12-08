from flask import Blueprint, request, render_template, session
from bson import ObjectId
import Constants
from models import Post
from routes.videoroutes.VideoUpload import uploadVideoHandler
from util import RouteRequirement
from util.GImage import GImage
from models.Video import Video

videoBlueprint = Blueprint("videoBlueprint", __name__)
serveVideoBlueprint = Blueprint("serveVideoBlueprint", __name__)
videoUploadBlueprint = Blueprint("videoUploadBlueprint", __name__)

VIDEO_PATH = 'storage/videos/'
videoObject = Video()
postRepo = Post.objects


@serveVideoBlueprint.route("/video/<videoID>")
@RouteRequirement.loginRequirement
def serveVideo(videoID):
    video = postRepo.filter(**{"_id": ObjectId(videoID)})
    path = VIDEO_PATH + video.filename
    return videoObject.partialRespoonse(request, path)


@videoUploadBlueprint.route("/videoupload", methods=["POST"])
@RouteRequirement.loginRequirement
def videoUpload():
    uploadVideoHandler()

    return "", 204
