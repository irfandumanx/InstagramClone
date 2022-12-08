from models import BaseModel


class Chat(BaseModel):
    def __init__(self, **kwargs):
        self._id = kwargs.get("_id", None)
        self.user1 = kwargs.get("user1")
        self.user2 = kwargs.get("user2")
        self.messages = kwargs.get("messages", [])

    def serialize(self, idOnly=True):
        if idOnly:
            return {"_id": self._id}
        return {"_id": self._id, "user1": self.user1, "user2": self.user2, "messages": self.messages}

    def __str__(self) -> str:
        return self.serialize(idOnly=False).__str__()

    def getTableName(self) -> str:
        return "chat"
