import os

from flask import session, request
from werkzeug.utils import secure_filename, redirect

from models import Post, User
from routes.routeutil.FileUtils import photoAllowedFile

UPLOAD_FOLDER = "storage/photos"
postRepo = Post.objects
userRepo = User.objects


def postUploadHandler():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if not (photoAllowedFile(file.filename)):
        return redirect(request.url)
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    post = postRepo.insert(**{"filename": filename, "likes": []})
    userRepo.pushUpdate(session["user"]["_id"], **{"posts": post.inserted_id})
