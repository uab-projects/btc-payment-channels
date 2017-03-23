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

    @classmethod
    def deserialize(cls, data):
        """
        Deserializes the contents of the data passed to try make them fit into
        the class model. If the data has invalid length or invalid data,
        appropiate exceptions will be raised.

        Please implement this method in a way that can receive more data than
        the strictly required in variable sized fields, so it will help caller
        methods to detect size after calling deserialization

        As a class method, the method returns an instance of a filled object

        Args:
            cls (class): class of the object to deserialize
            data (bytes): a bytes object containing data to de-serialize

        Returns:
            cls(): an instance of the class filled with the data if succeeded

        Raises:
            ValueError: if data can't be fit into the model
        """
        raise NotImplementedError("""Class should have implemented this, but"""
                                  """ developers of the app aren't so fast""")


class Encodable(object):
    """
    This interface defines that classes who inherit from it can be encoded into
    an object and decoded from an object. The difference between the previous
    class is that the serializable class is supposed to serialize to bytes
    objects and be deserialized from them. An encodable class when encoded
    contains enough information to then decode the output and obtain the same
    information but with the difference that when encoding, the result is not
    an array of bytes and is an object, most times a string.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def encode(self):
        """
        Encodes the information of the class into an object so that this object
        can be then decoded into another object of this class with the same
        information

        Returns:
            object: object containing the encoded information of the class
        """
        pass

    @classmethod
    def decode(cls, obj):
        """
        Decodes the object passed and tries to set the attributes and status of
        the object according to the data the object passed contains into a new
        object of the class

        Args:
            cls (class): class to decode the object into
            obj (object): object containing information to set class status

        Returns:
            cls(): an object with the status filled

        Raises:
            ValueError: if object passed can't be decoded
        """
        pass


class Base58Encodable(Encodable):
    """
    Same as previous Encodable interface, but specifies that will be encoded
    into a base58 string and decoded from a base58 string.
    """
