#!/usr/bin/python3
"""Unittest test_user module"""

import unittest
import pycodestyle
from models.engine.file_storage import FileStorage
from models.user import User


class TestUser(unittest.TestCase):
    """Test cases for TestUser class"""

    @classmethod
    def setUpClass(cls):
        """Set up class"""
        cls.storage = FileStorage()
        cls.user = User()
        cls.user.first_name = "Khaled"
        cls.user.last_name = "Ibn Al-Walid"
        cls.user.email = "unbeatable@leader.war"
        cls.user.password = "TheSwordOfGod"
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        """Clean up class"""
        del cls.storage
        del cls.user

    def test_pycodestyle(self):
        """Test that the code follows pycodestyle guidelines"""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/user.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self):
        """Test that the module has a docstring"""
        import models.user
        self.assertIsNotNone(models.user.__doc__)

    def test_class_docstring(self):
        """Test that the class has a docstring"""
        self.assertIsNotNone(User.__doc__)

    def test_user(self):
        """Test the User class"""
        all_objs = self.storage.all()
        key = f'User.{self.__class__.user.id}'
        self.assertIn(key, all_objs.keys())
