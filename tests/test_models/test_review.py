#!/usr/bin/python3
"""Unittest test_review module"""

import unittest
import pycodestyle
from models.engine.file_storage import FileStorage
from models.review import Review


class TestReview(unittest.TestCase):
    """Test cases for TestReview class"""

    @classmethod
    def setUpClass(cls):
        """Set up class"""
        cls.storage = FileStorage()
        cls.review = Review()
        cls.review.place_id = "0001"
        cls.review.user_id = "0002"
        cls.review.text = "Great place, had a wonderful time!"
        cls.review.save()

    @classmethod
    def tearDownClass(cls):
        """Clean up class"""
        del cls.storage
        del cls.review

    def test_pycodestyle(self):
        """Test that the code follows pycodestyle guidelines"""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/review.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self):
        """Test that the module has a docstring"""
        import models.review
        self.assertIsNotNone(models.review.__doc__)

    def test_class_docstring(self):
        """Test that the class has a docstring"""
        self.assertIsNotNone(Review.__doc__)

    def test_review(self):
        """Test the Review class"""
        all_objs = self.storage.all()
        key = f'Review.{self.__class__.review.id}'
        self.assertIn(key, all_objs.keys())
