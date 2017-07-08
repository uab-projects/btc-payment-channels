# -*- coding: utf-8 -*-
"""
Defines a model for all bitcoin protocol fields
"""
# Libraries
# # App
from ..interfaces import Serializable


# Data type model
class Field(Serializable):
    """
    Defines a model for what every defined field should provide. It should
    provide a variable where to store the value for the field, methods for its
    serialization and deserialization, a method to know the size in bytes and
    optionally a name and description for documentation and educational
    purposes

    The name and description should be class variables as all instances of same
    class will share their meaning. In some cases, though, name and description
    could be tied to the instance

    Attributes:
        value: value of the field, that can handle multiple data types
    """
    __slots__ = ["_value"]

    def __init__(self, value=None):
        """
        Initializes the field and assigns it a value, or None if no value is
        entered (useful for deserialization)

        Args:
            value: value to set the field to
        """
        self._value = value

    @property
    def value(self):
        """
        Returns the field value, as is

        Returns:
            the value of the field, usable in Python (not a bytes object!)
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Saves a new value into the field

        Args:
            value: the new value to set into the field

        Raises:
            ValueError: if the value can't be saved in this field
        """
        self._value = value

    def __len__(self):
        """
        Returns the size of the field in bytes, with the content that is
        present in the value if the size is variable for the field.

        By default, serializes and returns the bytes object length

        Returns:
            int: number of bytes the serialized field would occupy
        """
        return len(self.serialize())

    def __str__(self):
        """ Returns the field as a printable string """
        return "<%s:%s(%s)>" % (self.serialize().hex(),
                                self.__class__.__name__, self._value)

    def serialize(self):
        raise NotImplementedError("""Class should have implemented this, but"""
                                  """ developers of the app aren't so fast""")

    @classmethod
    def deserialize(self, data):
        raise NotImplementedError("""Class should have implemented this, but"""
                                  """ developers of the app aren't so fast""")
