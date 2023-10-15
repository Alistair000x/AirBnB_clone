#!/usr/bin/python3

import cmd
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage
import re
import json

class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "
    
    valid_classes = {
        "BaseModel": BaseModel,
        "User": User,
        "Place": Place,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Review": Review
    }

    def do_EOF(self, arg):
        """Exit the program with Ctrl-D"""
        return True

    def do_quit(self, arg):
        """Exit the program"""
        return True

    def emptyline(self):
        """Do nothing on an empty line"""
        pass

    def do_create(self, arg):
        """Create a new instance. Usage: create <class name>"""
        if not arg:
            print("** class name missing **")
        elif arg in HBNBCommand.valid_classes:
            new_instance = HBNBCommand.valid_classes[arg]()
            new_instance.save()
            print(new_instance.id)
        else:
            print("** class doesn't exist **")

    def do_clear(self, arg):
        """Clear all data storage. Usage: clear"""
        storage.all().clear()
        storage.save()
        self.do_all(arg)
        print("** All data has been cleared! **")

    def valid(self, args):
        """Check if the argument is valid"""
        if not args:
            print("** class name missing **")
            return False

        class_name = args[0]
        if class_name not in HBNBCommand.valid_classes:
            print("** class doesn't exist **")
            return False

        return True

    def do_show(self, arg):
        """Show the string representation of an instance. Usage: show <class name> <id>"""
        args = arg.split()
        if self.valid(args):
            class_name = args[0]
            instance_id = args[1]
            key = class_name + "." + instance_id
            if key in storage.all():
                print(storage.all()[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """Destroy an instance. Usage: destroy <class name> <id>"""
        args = arg.split()
        if self.valid(args):
            class_name = args[0]
            instance_id = args[1]
            key = class_name + "." + instance_id
            if key in storage.all():
                del storage.all()[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """Print all string representations of instances. Usage: all [class name]"""
        objects = storage.all().values()
        if arg:
            class_name = arg.split()[0]
            objects = [obj for obj in objects if obj.__class__.__name__ == class_name]

        print([str(obj) for obj in objects])

    def do_update(self, arg):
        """Update an instance with a new attribute or value. Usage: update <class name> <id> <attribute name> <attribute value>"""
        args = arg.split()
        if self.valid(args):
            class_name = args[0]
            instance_id = args[1]
            key = class_name + "." + instance_id

            if key in storage.all():
                if len(args) < 4:
                    print("** attribute name missing **")
                elif len(args) < 5:
                    print("** value missing **")
                else:
                    attribute_name = args[2]
                    attribute_value = args[3]
                    obj = storage.all()[key]

                    # Try to cast attribute value to int or float
                    if attribute_name in BaseModel.integer_fields:
                        attribute_value = int(attribute_value)
                    elif attribute_name in BaseModel.float_fields:
                        attribute_value = float(attribute_value)

                    setattr(obj, attribute_name, attribute_value)
                    obj.save()
            else:
                print("** no instance found **")

    def default(self, arg):
        """Handle advanced commands"""
        match = re.match(r'^(\w+)\.(\w+)\(([^)]*)\)', arg)
        if match:
            class_name = match.group(1)
            command = match.group(2)
            args = match.group(3).split(',')

            if class_name in HBNBCommand.valid_classes:
                if command == "all":
                    self.do_all(class_name)
                elif command == "count":
                    self.count(class_name)
                elif command == "show" and len(args) == 1:
                    self.do_show(class_name + ' ' + args[0])
                elif command == "destroy" and len(args) == 1:
                    self.do_destroy(class_name + ' ' + args[0])
                elif command == "update" and len(args) == 2:
                    self.do_update(class_name + ' ' + args[0] + ' ' + args[1])
                elif command == "update" and len(args) == 3:
                    value = re.search(r'[^"]+', args[2]).group()
                    self.do_update(class_name + ' ' + args[0] + ' ' + args[1] + ' "' + value + '"')
        else:
            super().default(arg)

if __name__ == "__main__":
    HBNBCommand().cmdloop()
