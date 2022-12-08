import asyncio
import json

import websockets

from models import User
from models import Post
from routes.routeutil.FileUtils import videoAllowedFile
from util import RouteRequirement
from flask import Flask, render_template, session
from routes.UserRoutes import userBlueprint
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from routes.ChatRoutes import chatBlueprint
from util.GImage import GImage
from routes.VideoRoutes import serveVideoBlueprint, videoBlueprint, videoUploadBlueprint
from routes.PostRoutes import photoBlueprint

app = Flask(__name__)
app.secret_key = "gof_instagram"

# Register the other routes
app.register_blueprint(videoUploadBlueprint)
app.register_blueprint(videoBlueprint)
app.register_blueprint(serveVideoBlueprint)
app.register_blueprint(photoBlueprint)
app.register_blueprint(userBlueprint)
app.register_blueprint(chatBlueprint)

userRep = User.objects
postRep = Post.objects


@app.route("/")
@RouteRequirement.loginRequirement
def indexPage():
    userWithPost = dict()  # key post id, value user
    userIdentity = User(**session["user"])

    users = userRep.getAll("profile_image_path", "username", "posts")
    for jData in users:
        user = User(**jData)
        lenUserPost = len(user.posts)
        if lenUserPost != 0:
            user.profileImage = GImage.decodeBase64FromPathWithExtension(user.profileImage)

            for i in range(0, lenUserPost):
                postID = user.posts[i]
                userWithPost[postID] = user

    tempUserDict = {**userWithPost}
    tempUserDict = sorted(tempUserDict.items(), reverse=True)

    for userTup in tempUserDict:
        isLike = False
        isVideo = False
        post = postRep.filter(**{"_id": userTup[0]})
        if videoAllowedFile(post.filename):
            isVideo = True
        postBase64 = GImage.decodeBase64FromPathWithExtension(post.filename)
        for id in post.likes:
            if session["user"]["_id"] == id:
                isLike = True
        postName = str(post._id) + "+irfan+" + postBase64["extension"] + "+irfan+" + postBase64[
            "src"] + "+irfan+" + str(isLike) + "+irfan+" + str(len(post.likes)) + "+irfan+" + str(isVideo)
        userWithPost[postName] = userWithPost[userTup[0]]
        del userWithPost[userTup[0]]

    return render_template("index.html", userMap=userWithPost, user=userIdentity,
                           image=GImage.decodeBase64FromPathWithExtension(userIdentity.profileImage))


chatsUser = {}
userWebsocket = dict()


async def handler(websocket):
    async for msg in websocket:
        data = json.loads(msg)

        if data["me"]["type"] == "socket":
            userWebsocket[data["me"]["user_id"]] = websocket
            continue
        elif data["me"]["type"] == "disconnect":
            for chatID, chat in dict(chatsUser).items():
                if chat["ready"]:
                    user1 = chat["user1"]["_id"]
                    user2 = chat["user2"]["_id"]
                    sessionUserID = data["me"]["user_id"]
                    if user1 == sessionUserID:
                        await chat["user2"]["socket"].send(
                            json.dumps({"me": {"type": "disconnect", "chat_id": chatID}}))
                        chatsUser.pop(chatID)

                    elif user2 == sessionUserID:
                        await chat["user1"]["socket"].send(
                            json.dumps({"me": {"type": "disconnect", "chat_id": chatID}}))
                        chatsUser.pop(chatID)
            continue
        elif data["me"]["type"] == "new-chat":
            otherUser = userRep.filter(**{"username": data["me"]["other_username"]})
            if otherUser._id in userWebsocket:
                user = userRep.filter(**{"_id": data["me"]["user_id"]})
                data["me"]["profileImage"] = GImage.decodeBase64FromPathWithExtension(user.profileImage)
                data["me"]["username"] = user.username
                await userWebsocket[otherUser._id].send(json.dumps(data))
            continue

        chatID = data["me"]["chat_id"]
        if chatsUser.get(chatID, None) is None:
            chatsUser[chatID] = {"user1": {"_id": data["me"]["user_id"], "socket": websocket}, "user2": None,
                                 "ready": False}
            await chatsUser[chatID]["user1"]["socket"].send(json.dumps({"me": {"type": "created", "chat_id": chatID}}))
        else:
            if chatsUser[chatID]["ready"]:
                if data["me"]["type"] == "call-open" or data["me"]["type"] == "call-answered":
                    user1 = chatsUser[chatID]["user1"]["_id"]
                    user2 = chatsUser[chatID]["user2"]["_id"]
                    sessionUserID = data["me"]["user_id"]
                    if user1 == sessionUserID:
                        await chatsUser[chatID]["user2"]["socket"].send(msg)
                    elif user2 == sessionUserID:
                        await chatsUser[chatID]["user1"]["socket"].send(msg)

                if "rtc" not in data:
                    continue
                elif data["rtc"]["type"] == "offer":
                    await chatsUser[chatID]["user2"]["socket"].send(msg)
                elif data["rtc"]["type"] == "answer":
                    await chatsUser[chatID]["user1"]["socket"].send(msg)
                elif data["rtc"]["type"] == "candidate":
                    await chatsUser[chatID]["user1"]["socket"].send(msg)
                    await chatsUser[chatID]["user2"]["socket"].send(msg)

            else:
                if chatsUser[chatID]["user1"]["_id"] == data["me"]["user_id"]:
                    continue
                chatsUser[chatID]["user2"] = {"_id": data["me"]["user_id"],
                                              "socket": websocket}
                chatsUser[chatID]["ready"] = True
                await chatsUser[chatID]["user2"]["socket"].send(
                    json.dumps({"me": {"type": "joined", "chat_id": chatID}}))
                await chatsUser[chatID]["user1"]["socket"].send(
                    json.dumps({"me": {"type": "ready", "chat_id": chatID}}))
                await chatsUser[chatID]["user2"]["socket"].send(
                    json.dumps({"me": {"type": "ready", "chat_id": chatID}}))


async def main():
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(8080)
    async with websockets.serve(handler, "localhost", 8081):
        await asyncio.Future()  # run forever
    # FLASK RUN
    # app.run(host=HOST, port=5500, debug=True)


if __name__ == "__main__":
    asyncio.run(main())
