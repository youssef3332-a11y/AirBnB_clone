#!/usr/bin/python3
""" storage module """
import json
import os
from models.base_model import BaseModel
from models.user import User


class FileStorage:
    """this class is responsible for storing objects
    instead of a database
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """dict returned"""
        return self.__objects

    def new(self, obj):
        """ add new object"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """save a json file"""
        jdict = {key: value.to_dict() for key, value in self. __objects.items()}
        with open(self.__file_path, 'w') as file:
            json.dump(jdict, file)

    def reload(self):
        """reload from the file"""
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r') as file:
                json_dic = json.load(file)
            for key, obj in json_dic.items():
                name = obj["__class__"]
                cls = globals()[name]
                self.__objects[key] = cls(**obj)
