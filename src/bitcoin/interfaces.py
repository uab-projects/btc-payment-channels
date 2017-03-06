# -*- coding: utf-8 -*-
"""
Defines functional models as interfaces to specify the functionality some
classes must provide.
"""

# Libraries
from abc import ABCMeta, abstractmethod


class Serializable(object):
    """
    Defines a model for a class that will be serializable, this means, will
    have methods to transform the class into an array of bytes and to create
    a new class using an array of bytes.

    Those arrays of bytes will always have to be compatible with the bytes
    specified in the Bitcoin protocol

    The arrays of bytes must be an instance of Python 3 bytes object
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def serialize(self):
        """
        Serializes the contents of the current class into an array of bytes so
        the class can be represented as an array of bytes compatible with what
        the Bitcoin protocol specifies

        Returns:
            bytes: data of the class serialized in a bytes object
        """
        raise NotImplementedError("""Class should have implemented this, but"""
                                  """ developers of the app aren't so fast""")

    @abstractmethod
    def deserialize(self, data):
        """
        Deserializes the contents of the data passed to try make them fit into
        the class model. If the data has invalid length or invalid data,
        appropiate exceptions will be raised.

        Please implement this method in a way that can receive more data than
        the strictly required in variable sized fields, so it will help caller
        methods to detect size after calling deserialization

        Args:
            data (bytes): a bytes object containing data to de-serialize

        Returns:
            the instance of the class filled with the data if succeeded

        Raises:
            ValueError: if data can't be fit into the model
        """
        raise NotImplementedError("""Class should have implemented this, but"""
                                  """ developers of the app aren't so fast""")
