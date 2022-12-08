from bson import ObjectId


class Message:
    def __init__(self, **kwargs):
        self._id = kwargs.get("_id", ObjectId())
        self.sender = kwargs.get("sender")
        self.message = kwargs.get("message")

    def serialize(self, idOnly=True):
        if idOnly:
            return {"_id": self._id}
        return {"_id": self._id, "sender": self.sender, "message": self.message}

    def __str__(self) -> str:
        return self.serialize(idOnly=False).__str__()
