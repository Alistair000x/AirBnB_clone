#!/usr/bin/python3
"""Unittest test_city module"""

import unittest
import pycodestyle
from models.engine.file_storage import FileStorage
from models.city import City


class TestCity(unittest.TestCase):
    """Test cases for TestCity class"""

    @classmethod
    def setUpClass(cls):
        """Set up class"""
        cls.storage = FileStorage()
        cls.city = City()
        cls.city.state_id = "R"
        cls.city.name = "Al Hoceima"
        cls.city.save()

    @classmethod
    def tearDownClass(cls):
        """Clean up class"""
        del cls.storage
        del cls.city

    def test_pycodestyle(self):
        """Test that the code follows pycodestyle guidelines"""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/city.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self):
        """Test that the module has a docstring"""
        import models.city
        self.assertIsNotNone(models.city.__doc__)

    def test_class_docstring(self):
        """Test that the class has a docstring"""
        self.assertIsNotNone(City.__doc__)

    def test_city(self):
        """Test the City class"""
        all_objs = self.storage.all()
        key = f'City.{self.__class__.city.id}'
        self.assertIn(key, all_objs.keys())
