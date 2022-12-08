import re

from bson import ObjectId
from flask import Blueprint, render_template, session, request
from pymongo.cursor import Cursor
from pymongo.results import InsertOneResult

from models import User
from models.Chat import Chat
from models.Message import Message
from util import RouteRequirement
from util.GDate import GDate
from util.GImage import GImage

chatBlueprint = Blueprint("chatBlueprint", __name__)
userRepo = User.objects
chatRepo = Chat.objects


def getPersons():
    user = User(**session["user"])
    chats = list(chatRepo.getAll("_id", "user1", "user2", "messages", **{"$or": [{"user1": user._id},
                                                                                 {"user2": user._id}]}))
    chatHtml = list()
    for chat in chats[::-1]:
        mainUser = user._id
        if mainUser == chat["user1"]:
            otherUser = chat["user2"]
        else:
            otherUser = chat["user1"]

        otherUser = userRepo.filter(**{"_id": otherUser})
        lastMessage = ""
        chatLen = len(chat["messages"])
        time = None
        if chatLen != 0:
            last = chat["messages"][chatLen - 1]
            lastMessage = last["message"]
            time = GDate.getTimeDifference(last["_id"].generation_time)

        chatHtml.append({"chatID": str(chat["_id"]), "name": otherUser.name, "username": otherUser.username,
                         "lastMessage": lastMessage, "time": time,
                         "image": GImage.decodeBase64FromPathWithExtension(otherUser.profileImage)})
    return chatHtml


@chatBlueprint.route("/chat")
@RouteRequirement.loginRequirement
def chat():
    user = User(**session["user"])
    return render_template("chat.html", chatHtml=getPersons(), user=user,
                           image=GImage.decodeBase64FromPathWithExtension(user.profileImage))


@chatBlueprint.route("/new-message", methods=["POST"])
def newMessage():
    user = User(**session["user"])
    otherUser = userRepo.filter(**{"username": request.form.get("username")})
    chatID = chatRepo.insert(**{"user1": user._id, "user2": otherUser._id, "messages": []})
    return {"chatID": str(chatID.inserted_id), "name": otherUser.name, "username": otherUser.username,
            "image": GImage.decodeBase64FromPathWithExtension(otherUser.profileImage)}


@chatBlueprint.route("/chat/<chatID>", methods=["GET", "POST"])
def getMessages(chatID):
    user = User(**session["user"])
    if request.method == "POST":
        chatRepo.pushUpdate(ObjectId(chatID), **{
            "messages": Message(sender=user.username, message=request.form.get("message")).serialize(idOnly=False)})
        return "", 204

    chat = chatRepo.filter(**{"_id": ObjectId(chatID)})
    if chat.user1 == user._id:
        otherUser = chat.user2
    else:
        otherUser = chat.user1
    otherUser = userRepo.filter(**{"_id": otherUser})
    return render_template("chatinner.html", messages=chat.messages, otherUser=otherUser, chatHtml=getPersons(),
                           user=user,
                           image=GImage.decodeBase64FromPathWithExtension(user.profileImage),
                           otherUserImage=GImage.decodeBase64FromPathWithExtension(otherUser.profileImage))
