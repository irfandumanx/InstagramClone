from abc import ABC, abstractmethod

from database.ObjectManager import ObjectManagerFactory
from database import ObjectManager


class BaseModel(ABC):
    def __init_subclass__(cls, **kwargs) -> None:
        cls.objects: ObjectManager = ObjectManagerFactory[cls, BaseModel]()

    @abstractmethod
    def serialize(self, idOnly=True):
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def getTableName(self) -> str:
        raise NotImplementedError

