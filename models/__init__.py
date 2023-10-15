#!/usr/bin/python3
"""Auto __init__ script"""

from models.engine.file_storage import FileStorage

# Create a FileStorage instance
storage = FileStorage()

# Reload data from the JSON file (if it exists)
storage.reload()
