#!/usr/bin/python3
"""Unittest test_place module"""

import unittest
import pycodestyle
from models.engine.file_storage import FileStorage
from models.place import Place


class TestPlace(unittest.TestCase):
    """Test cases for TestPlace class"""

    @classmethod
    def setUpClass(cls):
        """Set up class"""
        cls.storage = FileStorage()
        cls.place = Place()
        cls.place.city_id = "0001"
        cls.place.user_id = "0002"
        cls.place.name = "My place"
        cls.place.description = "A cozy place in the city"
        cls.place.number_rooms = 2
        cls.place.number_bathrooms = 1
        cls.place.max_guest = 4
        cls.place.price_by_night = 100
        cls.place.latitude = 37.7749
        cls.place.longitude = -122.4194
        cls.place.amenity_ids = ["0003", "0004"]
        cls.place.save()

    @classmethod
    def tearDownClass(cls):
        """Clean up class"""
        del cls.storage
        del cls.place

    def test_pycodestyle(self):
        """Test that the code follows pycodestyle guidelines"""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/place.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self):
        """Test that the module has a docstring"""
        import models.place
        self.assertIsNotNone(models.place.__doc__)

    def test_class_docstring(self):
        """Test that the class has a docstring"""
        self.assertIsNotNone(Place.__doc__)

    def test_place(self):
        """Test the Place class"""
        all_objs = self.storage.all()
        key = f'Place.{self.__class__.place.id}'
        self.assertIn(key, all_objs.keys())
