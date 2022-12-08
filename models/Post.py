from models import BaseModel


class Post(BaseModel):
    def __init__(self, **kwargs):
        self._id = kwargs.get("_id", None)
        self.filename = kwargs.get("filename")
        self.likes = kwargs.get("likes", [])

    def serialize(self, idOnly=True):
        if idOnly:
            return {"_id": self._id}
        return {"_id": self._id, "filename": self.filename, "likes": self.likes}

    def checkIsLike(self, userID):
        isLike = False

        for id in self.likes:
            if userID == id:
                isLike = True

        return isLike

    def __str__(self) -> str:
        return self.serialize(idOnly=False).__str__()

    def getTableName(self) -> str:
        return "posts"
