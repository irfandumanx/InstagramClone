import os
from threading import Thread
import Constants
from flask import copy_current_request_context, request, session
from werkzeug.utils import secure_filename, redirect

from models import Post, User
from routes.routeutil.FileUtils import videoAllowedFile
from routes.routeutil.VideoUtils import getVideoPhoto

VIDEO_FOLDER = "storage/videos"
VIDEO_PHOTO_FOLDER = "storage/videophotos"

postRepo = Post.objects
userRepo = User.objects


def uploadVideoHandler():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if not (videoAllowedFile(file.filename)):
        redirect(request.url)

    @copy_current_request_context
    def saveFile(closeAfterWrite):
        filename = secure_filename(file.filename)
        file.save(os.path.join(VIDEO_FOLDER, filename))
        getVideoPhoto(filename, VIDEO_PHOTO_FOLDER)
        post = postRepo.insert(**{"filename": filename, "likes": []})
        userRepo.pushUpdate(session["user"]["_id"], **{"posts": post.inserted_id})
        closeAfterWrite()

    def passExit():
        pass

    normalExit = file.stream.close
    file.stream.close = passExit
    t = Thread(target=saveFile, args=(normalExit,))
    t.start()
    return '', 204
