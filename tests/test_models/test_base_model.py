#!/usr/bin/python4
import unittest
from datetime import datetime
import time

# Import the BaseModel class from the module where it's defined
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import json
import os


class TestBaseModel(unittest.TestCase):
    def setUp(self):
        """Set up test case environment."""
        self.storage = FileStorage(file_path="test_file.json")
        self.storage._FileStorage__objects = {}
        self.model = BaseModel()
    
    def tearDown(self):
        """Clean up after each test."""
        try:
            os.remove("test_file.json")
        except FileNotFoundError:
            pass

    def test_id(self):
        """Test that id is a string and has a UUID format."""
        self.assertIsInstance(self.model.id, str)
        self.assertRegex(self.model.id, r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')

    def test_created_at(self):
        """Test that created_at is a datetime object."""
        self.assertIsInstance(self.model.created_at, datetime)

    def test_updated_at(self):
        """Test that updated_at is a datetime object."""
        self.assertIsInstance(self.model.updated_at, datetime)

    def test_str(self):
        """Test the __str__ method."""
        expected_str = "[BaseModel] ({}) {}".format(self.model.id, self.model.__dict__)
        self.assertEqual(str(self.model), expected_str)

    def test_save(self):
        """Test that save method updates updated_at."""
        old_updated_at = self.model.updated_at
        time.sleep(1)  # Ensure a time difference
        self.model.save()
        self.assertNotEqual(self.model.updated_at, old_updated_at)
        self.assertGreater(self.model.updated_at, old_updated_at)

    def test_to_dict(self):
        """Test the to_dict method."""
        model_dict = self.model.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertEqual(model_dict['__class__'], 'BaseModel')
        self.assertEqual(model_dict['created_at'], self.model.created_at.isoformat())
        self.assertEqual(model_dict['updated_at'], self.model.updated_at.isoformat())
    def test_dict_to_class(self):
        """test the task"""
        model_dict = self.model.to_dict()
        new = BaseModel(**model_dict)
        self.assertIsInstance(new, BaseModel)
        self.assertEqual(self.model.__dict__, new.__dict__)
    
    def test_new_method(self):
        """Test new method."""
        # Add the base model to the storage
        self.storage.new(self.base_model)
        
        # Retrieve all objects from storage
        all_objects = self.storage.all()
        
        # Check if the object is correctly stored
        key = f"BaseModel.{self.base_model.id}"
        self.assertIn(key, all_objects)
        self.assertEqual(all_objects[key], self.base_model)

    def test_all_method(self):
        """Test all method."""
        # Add the base model to the storage
        self.storage.new(self.base_model)
        
        # Retrieve all objects from storage
        all_objects = self.storage.all()
        
        # Check if the object is correctly stored
        key = f"BaseModel.{self.base_model.id}"
        self.assertIn(key, all_objects)
        self.assertEqual(all_objects[key], self.base_model)

    def test_save_method(self):
        """Test save method."""
        # Add dynamic attributes
        self.base_model.name = "My_First_Model"
        self.base_model.my_number = 89
        
        # Add the base model to the storage
        self.storage.new(self.base_model)
        
        # Save the storage to a file
        self.storage.save()
        
        # Check if the file was created
        self.assertTrue(os.path.exists("test_file.json"))
        
        # Load the JSON data
        with open("test_file.json", "r") as f:
            data = json.load(f)
        
        # Check the stored data
        key = f"BaseModel.{self.base_model.id}"
        self.assertIn(key, data)
        self.assertEqual(data[key]['name'], "My_First_Model")
        self.assertEqual(data[key]['my_number'], 89)
        self.assertEqual(data[key]['__class__'], 'BaseModel')

    def test_reload_method(self):
        """Test reload method."""
        # Add dynamic attributes
        self.base_model.name = "My_First_Model"
        self.base_model.my_number = 89
        
        # Add the base model to the storage
        self.storage.new(self.base_model)
        
        # Save the storage to a file
        self.storage.save()
        
        # Create a new FileStorage instance to simulate reloading
        new_storage = FileStorage(file_path="test_file.json")
        new_storage.reload()
        
        # Retrieve all objects from the new storage
        all_objects = new_storage.all()
        
        # Check if the object is correctly reloaded
        key = f"BaseModel.{self.base_model.id}"
        self.assertIn(key, all_objects)
        reloaded_model = all_objects[key]
        self.assertEqual(reloaded_model.name, "My_First_Model")
        self.assertEqual(reloaded_model.my_number, 89)
        self.assertEqual(reloaded_model.id, self.base_model.id)
        self.assertEqual(reloaded_model.__class__.__name__, 'BaseModel')

if __name__ == '__main__':
    unittest.main()

