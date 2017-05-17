"""
Methods that allows fields to be tested and check that work following the
Bitcoin protocol standards
"""
# Libraries
# # App
from .helper import value_to_hex


# Test classes
def serialization(deserialized, serialized, cls):
    """
    Given a correct known deserialized value and its serialized value, checks
    against the class given if the serialization method is properly implemented
    or raises a ValueError if not

    Args:
        deserialized (object): python object corresponding to serialized bytes
        serialized (bytes): value properly serialized as bytes
        cls (class): python class to check serialization method against

    Raises:
        ValueError if serialization fails
    """
    # Show value to serialize and solution
    print("Serializing the value", value_to_hex(deserialized))
    # Do serialization
    serialized_guess = cls(deserialized).serialize()
    # Check it
    if serialized_guess != serialized:
        raise ValueError("Serialization failed: " +
                         value_to_hex(serialized_guess) +
                         " has to be "+value_to_hex(serialized))


def deserialization(deserialized, serialized, cls):
    """
    Given a correct known deserialized value and its serialized value, checks
    against the class given if the deserialization method is properly
    implemented or raises a ValueError if not

    Args:
        deserialized (object): python object corresponding to serialized bytes
        serialized (bytes): value properly serialized as bytes
        cls (class): python class to check deserialization method against

    Raises:
        ValueError if deserialization fails
    """
    print("Deserializing the value", value_to_hex(serialized))
    deserialized_guess = cls.deserialize(serialized).value
    if deserialized_guess != deserialized:
        raise ValueError("Deserialization failed: " +
                         value_to_hex(deserialized_guess) + " has to be " +
                         value_to_hex(deserialized))


def serialize_deserialize(*args):
    """
    Given a correct known deserialized value and its serialized value, checks
    against the class given if the serialization and deserialization methods
    are properly implemented or raises a ValueError if not

    Args:
        deserialized (object): python object corresponding to serialized bytes
        serialized (bytes): value properly serialized as bytes
        cls (class): python class to check serialization / deserialization
                     methods against

    Raises:
        ValueError if serialization or deserialization fails
    """
    serialization(*args)
    deserialization(*args)
