from uuid import uuid4
from models.BaseModel import BaseModel


class User(BaseModel):
    def __init__(self, **kwargs):
        self._id = kwargs.get("_id", uuid4().hex)
        self.email = kwargs.get("email")
        self.username = kwargs.get("username")
        self.name = kwargs.get("name")
        self.password = kwargs.get("password", "")
        self.createdOn = kwargs.get("created_on")  # create date update date delete date
        self.profileImage = kwargs.get("profile_image_path", "img_avatar.png")
        self.posts = kwargs.get("posts", {})
        self.mailValidationCode = kwargs.get("email_validation")

    def serialize(self, idOnly=True):
        if idOnly:
            return {"_id": self._id}
        return {"_id": self._id, "email": self.email, "username": self.username, "name": self.name,
                "password": self.password, "created_on": self.createdOn,
                "profile_image_path": self.profileImage}

    def __str__(self) -> str:
        return self.serialize(idOnly=False).__str__()

    def getTableName(self) -> str:
        return "users"
