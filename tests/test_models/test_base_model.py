#!/usr/bin/python3
import unittest
from datetime import datetime
import time
import uuid
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    def setUp(self):
        self.model = BaseModel()

    def test_id_is_string(self):
        self.assertIsInstance(self.model.id, str)

    def test_id_is_valid_uuid(self):
        self.assertIsInstance(uuid.UUID(self.model.id), uuid.UUID)

    def test_created_at_is_datetime(self):
        self.assertIsInstance(self.model.created_at, datetime)

    def test_updated_at_is_datetime(self):
        self.assertIsInstance(self.model.updated_at, datetime)

    def test_id_is_unique(self):
        another_model = BaseModel()
        self.assertNotEqual(self.model.id, another_model.id)

class TestBaseModelStr(unittest.TestCase):
    def setUp(self):
        self.model = BaseModel()

    def test_str_format(self):
        expected_str = "[BaseModel] ({}) {}".format(self.model.id, self.model.__dict__)
        self.assertEqual(str(self.model), expected_str)

    def test_str_contains_class_name(self):
        self.assertIn("BaseModel", str(self.model))

    def test_str_contains_id(self):
        self.assertIn(self.model.id, str(self.model))

    def test_str_contains_dict(self):
        self.assertIn(str(self.model.__dict__), str(self.model))

    def test_str_is_not_empty(self):
        self.assertNotEqual(str(self.model), "")

class TestBaseModel_save(unittest.TestCase):
    def setUp(self):
        self.model = BaseModel()

    def test_save_updates_updated_at(self):
        old_updated_at = self.model.updated_at
        time.sleep(1)
        self.model.save()
        self.assertNotEqual(self.model.updated_at, old_updated_at)

    def test_save_updated_at_is_greater(self):
        old_updated_at = self.model.updated_at
        time.sleep(1)
        self.model.save()
        self.assertGreater(self.model.updated_at, old_updated_at)

    def test_save_multiple_times(self):
        old_updated_at = self.model.updated_at
        time.sleep(1)
        self.model.save()
        first_update = self.model.updated_at
        time.sleep(1)
        self.model.save()
        self.assertGreater(self.model.updated_at, first_update)
        self.assertGreater(first_update, old_updated_at)

    def test_save_does_not_change_created_at(self):
        old_created_at = self.model.created_at
        self.model.save()
        self.assertEqual(self.model.created_at, old_created_at)

    def test_save_updates_at_isoformat(self):
        self.model.save()
        updated_at_str = self.model.updated_at.isoformat()
        self.assertEqual(self.model.updated_at.isoformat(), updated_at_str)

class TestBaseModel_to_dict(unittest.TestCase):
    def setUp(self):
        self.model = BaseModel()

    def test_to_dict_is_dict(self):
        self.assertIsInstance(self.model.to_dict(), dict)

    def test_to_dict_contains_class(self):
        self.assertIn("__class__", self.model.to_dict())

    def test_to_dict_class_name(self):
        self.assertEqual(self.model.to_dict()["__class__"], "BaseModel")

    def test_to_dict_created_at_is_str(self):
        self.assertIsInstance(self.model.to_dict()["created_at"], str)

    def test_to_dict_updated_at_is_str(self):
        self.assertIsInstance(self.model.to_dict()["updated_at"], str)

if __name__ == '__main__':
    unittest.main()

