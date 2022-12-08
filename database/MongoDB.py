from database.Database import Database
from pymongo import MongoClient


# repository pattern cekcen buraya


class MongoDB(Database):
    __db = None

    def __init__(self, host, port, username="username", password="12345"):
        super().__init__(host=host, port=port, username=username, password=password)
        self.connect()

    def connect(self):
        client = MongoClient("mongodb://{host}:{port}/".format(host=self.host, port=self.port))
        self.__db = client.local

    def getAll(self, model, selectedFields, *args, **kwargs):
        return self.__db[model.getTableName()].find(kwargs, selectedFields)

    def filter(self, model, *args, **kwargs):
        return self.__db[model.getTableName()].find_one(kwargs)

    def setUpdate(self, model, *args, **kwargs):
        self.__db[model.getTableName()].update_one({"_id": args[0]}, {"$set": kwargs})

    def pushUpdate(self, model, *args, **kwargs):
        self.__db[model.getTableName()].update_one({"_id": args[0]}, {"$push": kwargs})

    def insert(self, model, *args, **kwargs):
        return self.__db[model.getTableName()].insert_one(kwargs)

    def save(self, model, *args, **kwargs):
        self.__db[model.getTableName()].replace_one({"_id": args[0]}, kwargs)
