#!/usr/bin/python3
"""Unittest test_amenity module"""

import unittest
import pycodestyle
from models.engine.file_storage import FileStorage
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """Test cases for TestAmenity class"""

    @classmethod
    def setUpClass(cls):
        """Set up class"""
        cls.storage = FileStorage()
        cls.storage.reload()

    @classmethod
    def tearDownClass(cls):
        """Clean up class"""
        del cls.storage

    def setUp(self):
        """Set up test cases"""
        self.amenity = Amenity()
        self.storage._FileStorage__objects = {}

    def tearDown(self):
        """Clean up after test cases"""
        del self.amenity

    def test_amenity(self):
        """Test the Amenity class"""
        my_amenity = self.amenity
        my_amenity.name = "Wifi"
        my_amenity.save()

        all_objs = self.__class__.storage.all()
        key = f'Amenity.{my_amenity.id}'
        self.assertIn(key, all_objs.keys())

    def test_pycodestyle(self):
        """Test that the code follows pycodestyle guidelines"""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/amenity.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self):
        """Test that the module has a docstring"""
        import models.amenity
        self.assertIsNotNone(models.amenity.__doc__)

    def test_class_docstring(self):
        """Test that the class has a docstring"""
        self.assertIsNotNone(Amenity.__doc__)
