from abc import ABC, abstractmethod


class Database(ABC):
    def __init__(self, host="localhost", port=27017, username="username", password="12345", db_path="example.db"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db_path = db_path

    @abstractmethod
    def connect(self):
        raise NotImplementedError

    @abstractmethod
    def getAll(self, model, selectedFields, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def filter(self, model, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def setUpdate(self, model, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def pushUpdate(self, model, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def insert(self, model, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def save(self, model, *args, **kwargs):
        raise NotImplementedError
