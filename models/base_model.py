#!/usr/bin/python3
"""BaseModel class for Airbnb project."""
import uuid
import datetime
import models


class BaseModel:
    """BaseModel class for Airbnb project."""
    def __init__(self, *args, **kwargs):
        """constractor"""
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.datetime.fromisoformat(value)
                if key != "__class__":
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()
        models.storage.new(self)

    def __str__(self):
        """__str__ override"""
        name = self.__class__.__name__
        result = "[{}] ({}) {}".format(name, self.id, self.__dict__)
        return result

    def save(self):
        """ update date"""
        self.updated_at = datetime.datetime.now()
        models.storage.save()

    def to_dict(self):
        """to dictionary"""
        dit = self.__dict__.copy()
        dit["__class__"] = self.__class__.__name__
        dit['created_at'] = self.created_at.isoformat()
        dit['updated_at'] = self.updated_at.isoformat()
        return dit
