#!/usr/bin/python3
"""This module defines the State class"""

from models.base_model import BaseModel


class State(BaseModel):
    """State class that inherits from BaseModel"""

    name = ''

     def __init__(self, *args, **kwargs):
        """initializes State"""
        super().__init__(*args, **kwargs)

