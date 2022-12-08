import Constants
from Template import Template


@Template
def ObjectManagerFactory(model, parentModel):
    class ObjectManager:
        def __init__(self):
            if not issubclass(model, parentModel):
                raise TypeError("{} is not a subclass of {}".format(
                    model.__name__,
                    parentModel.__name__
                ))
            self.model = model()
            self.__db = Constants.CURRENT_DB

        def getAll(self, *args, **kwargs):
            selectedFields = {"_id": 0}
            for field in args:
                selectedFields[field] = 1

            return self.__db.getAll(self.model, selectedFields, *args, **kwargs)

        def filter(self, *args, **kwargs) -> model:
            response = self.__db.filter(self.model, *args, **kwargs)
            if response is None:
                return None
            return model(**response)

        def setUpdate(self, *args, **kwargs):
            self.__db.setUpdate(self.model, *args, **kwargs)

        def pushUpdate(self, *args, **kwargs):
            self.__db.pushUpdate(self.model, *args, **kwargs)

        def insert(self, *args, **kwargs):
            return self.__db.insert(self.model, *args, **kwargs)

        def save(self, *args, **kwargs):
            return self.__db.save(self.model, *args, **kwargs)

    return ObjectManager
