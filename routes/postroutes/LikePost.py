from flask import session

from models import Post
from bson import ObjectId

postRepo = Post.objects


def likeActionHandler(photoID):
    post = postRepo.filter(**{"_id": ObjectId(photoID)})
    likeCount = len(post.likes)
    userID = session["user"]["_id"]
    isLike = post.checkIsLike(userID)
    if isLike:
        post.likes.remove(userID)
        likeCount -= 1
    else:
        post.likes.append(userID)
        likeCount += 1
    postDict = post.serialize(idOnly=False)
    postRepo.save(post._id, **postDict)
    return {"like": not isLike, "likeCount": likeCount}
