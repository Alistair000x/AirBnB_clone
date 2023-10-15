#!/usr/bin/python3
"""Unittest test_console module"""

import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel

class TestConsole(unittest.TestCase):
    """TestHBNBCommand class"""

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
        self.console = HBNBCommand(stdin=StringIO(), stdout=StringIO())
        self.console.storage = self.__class__.storage
        self.storage._FileStorage__objects = {}

    def tearDown(self):
        """Clean up after test cases"""
        self.console.stdout.close()
        self.console.stdin.close()

    def test_module_docstring(self):
        """Test that the module has a docstring"""
        self.assertIsNotNone(__doc__)

    def test_class_docstring(self):
        """Test that the class has a docstring"""
        self.assertIsNotNone(HBNBCommand.__doc__)

    def test_quit_docstring(self):
        """Test that the quit method has a docstring"""
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)

    def test_EOF_docstring(self):
        """Test that the EOF method has a docstring"""
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)

    def test_emptyline_docstring(self):
        """Test that the emptyline method has a docstring"""
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)

    def test_pycodestyle(self):
        """Test that the code conforms to pycodestyle"""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0, "Found code style errors (and warnings).")

    def test_quit_command(self):
        """Test the quit command"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd('quit')
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, '')

    def test_EOF_command(self):
        """Test the EOF command"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd('EOF')
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, '')

    def test_emptyline_command(self):
        """Test the emptyline command"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd('')
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, '')

    def test_create_command(self):
        """Test the create command"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd('create')
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, '** class name missing **')

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd('create MyModel')
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, '** class doesn\'t exist **')

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd('create BaseModel')
            output = mock_stdout.getvalue().strip()
            all_objs = self.storage.all()
            key = f'BaseModel.{output}'
            self.assertIn(key, all_objs.keys())

    def test_show_command(self):
        """Test the show command"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd('show')
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, '** class name missing **')

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd('show MyModel')
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, '** class doesn\'t exist **')

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd('show BaseModel')
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, '** instance id missing **')

        my_model = BaseModel()
        my_model.save()

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            cmd = f'show BaseModel {my_model.id}'
            self.console.onecmd(cmd)
            output = mock_stdout.getvalue().strip()
            expected_output = str(my_model)
            self.assertEqual(output, expected_output)

    def test_destroy_command(self):
        """Test the destroy command"""
        my_model = BaseModel()
        my_model.save()

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd('destroy')
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, '** class name missing **')

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd('destroy MyModel')
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, '** class doesn\'t exist **')

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd('destroy BaseModel')
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, '** instance id missing **')

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            cmd = f'destroy BaseModel {my_model.id}'
            self.console.onecmd(cmd)
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, '')

        all_objs = self.storage.all()
        key = f'BaseModel.{my_model.id}'
        self.assertNotIn(key, all_objs.keys())

    def test_all_command(self):
        """Test the all command"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd('all')
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, '[]')

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd('all MyModel')
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, '** class doesn\'t exist **')

        my_model1 = BaseModel()
        my_model1.save()

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd('all')
            output = mock_stdout.getvalue().strip()
            expected_output = f'[\"{str(my_model1)}\"]'
            self.assertEqual(output, expected_output)

        my_model2 = BaseModel()
        my_model2.save()

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd('all')
            output = mock_stdout.getvalue().strip()
            expected_output1 = str(my_model1)
            expected_output2 = str(my_model2)
            self.assertIn(expected_output1, output)
            self.assertIn(expected_output2, output)

    def test_update_command(self):
        """Test the update command"""
        my_model = BaseModel()
        my_model.save()

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout
