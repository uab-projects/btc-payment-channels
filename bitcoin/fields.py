# -*- coding: utf-8 -*-
"""
Defines several data structures used in low-level bitcoin for carrying data
in the protocol as fields in transactions, blocks...

Classes defined here are only used inside the app to provide easy storage and
serialization, it's not inteded to use for the app user. This way, this classes
provided here should only be used to create data structure that will deal with
Python data types and may use this classes just to store them, knowing that
they will also provide serialization methods.

The following classes allow to deal with low-level data providing methods to
easily handle the data in fields and providing methods to transform them into
an array of bytes compatible with the Bitcoin standards definition and
vice-versa

For convention purposes, we'll use special notation when naming classes.
These prefixes may be applied:

 - Size prefix:
   Some fields have a fixed size. In this case, a prefix is added with the
   following components:
    - If the field has sign or not
      U for unsigned, S for signed
    - Field size in bytes
      The size followed by a B indicating it's the size in bytes
   Example: U4B specifies an unsigned 4 byte field
   If the field has no fixed size, then prefix Var is used

 - Endianness prefix:
   The prefix LE will be understood as little endian and BE for big endian.
   If nothing specified, big endian is used.

When naming classes, also a special convention will be used to specify the
data type it's containing:
 - Int: any number field, either positive or negative and size-independent
 - Str: any string field

Classes are added as needed so maybe many possible fields may exist in the
Bitcoin protocol but not available here because it's not used anywhere.
"""

# Libraries
import struct
from interfaces import Serializable


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
        Returns the size of the field in bytes, with the content that is present
        in the value if the size is variable for the field.

        By default, serializes and returns the bytes object length

        Returns:
            int: number of bytes the serialized field would occupy
        """
        return len(self.serialize())

    def serialize(self):
        raise NotImplementedError("""Class should have implemented this, but"""
                                  """ developers of the app aren't so fast""")
    def deserialize(self, data):
        raise NotImplementedError("""Class should have implemented this, but"""
                                  """ developers of the app aren't so fast""")

# Integer types
class S4BLEInt(Field):
    """
    Defines a Bitcoin protocol signed 4-byte integer field
    """
    name = "Signed 4-byte integer little-endian field (int32_t)"
    description = "32 bits with 2-complement sign"
    def __len__(self):
        return 4
    def serialize(self):
        return struct.pack('<l', self._value)
    def deserialize(self, v):
        self._value = struct.unpack('<l', v)[0]
        return self
    def __str__(self):
        return "0x{0:02x}".format(self._value)

class U4BLEInt(Field):
    """
    Defines a Bitcoin protocol unsigned 4-byte integer field
    """
    name = "Unsigned 4-byte integer little-endian field (uint32_t)"
    description = "32 bits without 2-complement sign"
    def __len__(self):
        return 4
    def serialize(self):
        return struct.pack('<L', self._value)
    def deserialize(self, v):
        self._value = struct.unpack('<L', v)[0]
        return self
    def __str__(self):
        return "0x{0:02x}".format(self._value)

class VarInt(Field):
    """
    Defines a Bitcoin protocol variable-sized integer field.

    It checks if the integer to save is lower than 0xFC (here BYTE_LIMIT)
    If it is, it saves it into 1 byte unsigned little-endian integer

    If not, the integer is saved the following way:
        [size][integer_value]

    Where size:
        0xFD (BYTE_LIMIT+1): to save an integer that fits in 2 bytes*
            *2 byte integers and 1 byte integers between 0xFD and 0xFF included
            (that are used as size prefixes)
        0xFE (BYTE_LIMIT+2): to save an integer that fits in 3-4 bytes
        0xFF (BYTE_LIMIT+3): to save an integer that fits in 5-8 bytes

    And integer value is the integer value coded as 2, 4, 8 byte unsigned
    little-endian integer depending on the size specified
    """
    BYTE_LIMIT = 0xFC
    name = "Bitcoin variable-length unsigned little-endian integer"
    description = "Allows to save an integer with variable size (1 to 9 bytes)"
    @classmethod
    def translate_size(cls, first_byte):
        """
        Given the first byte of a variable-sized integer, returns the size
        that the variable integer is occupying (excluding this first byte that
        indicates size)

        The values that can return are then 0 if just occupies this byte, 2 if
        occupies 2 bytes, 4 or 8.

        Args:
            firstByte (int): first byte of a var integer to calculate the size

        Returns:
            int: the size of the variable integer
        """
        return 2**(first_byte - cls.BYTE_LIMIT) if first_byte > cls.BYTE_LIMIT \
        else 0

    def __len__(self):
        if self._value <= self.BYTE_LIMIT:
            return 1
        elif self._value <= 0xFFFF:
            return 3
        elif self._value <= 0xFFFFFFFF:
            return 5
        else:
            return 9
    def serialize(self):
        if self._value <= self.BYTE_LIMIT:
            return struct.pack('<B', self._value)
        elif self._value <= 0xFFFF:
            return struct.pack('<BH', self.BYTE_LIMIT+1, self._value)
        elif self._value <= 0xFFFFFFFF:
            return struct.pack('<BL', self.BYTE_LIMIT+2, self._value)
        else:
            return struct.pack('<BQ', self.BYTE_LIMIT+3, self._value)
    def deserialize(self, v):
        size = self.translate_size(v[0])
        if size == 0:
            self._value = v[0]
        elif size == 2:
            self._value = struct.unpack('<H', v[1:3])[0]
        elif size == 4:
            self._value = struct.unpack('<L', v[1:5])[0]
        elif size == 8:
            self._value = struct.unpack('<Q', v[1:9])[0]
        else:
            raise ValueError("""Length of the deserialize variable integer """
                             """must be 1, 3, 5 or 9 bytes""")
        return self
    def __str__(self):
        return "0x{0:02x}".format(self._value)

class U8BLEInt(Field):
    """
    Defines a Bitcoin protocol unsigned 8-byte integer field
    """
    name = "Unsigned 8-byte integer little-endian field (uint64_t)"
    description = "64 bits without 2-complement sign"
    def serialize(self):
        return struct.pack('<Q', self._value)
    def deserialize(self, v):
        self._value = struct.unpack('<Q', v)[0]
        return self
    def __str__(self):
        return "0x{0:02x}".format(self._value)

def serialize_tests(deserialized, serialized, cls):
    """
    Given a serialized value and a checked deserialized value, checks against
    the class if the serialization and deserialization methods are properly
    implemented or raises a ValueError

    Args:
        deserialized (object): python object corresponding to serialized bytes
        serialized (bytes): serialized properly bytes
        cls (class): python class to check against

    Raises:
        ValueError if serialization or deserialization fails
    """
    # Serialization test
    print(" Serializing the value", "0x{0:02x}".format(deserialized))
    serialized_guess = cls(deserialized).serialize()
    if serialized_guess != serialized:
        raise ValueError("Serialization failed: "+serialized_guess.hex()+\
                         " != "+serialized.hex())
    # Deserialization test
    print(" Deserializing the value", serialized.hex())
    deserialized_guess = cls().deserialize(serialized).value
    if deserialized_guess != deserialized:
        raise ValueError("Deserialization failed: "+\
                         "0x{0:02x}".format(deserialized_guess)+\
                         " != "+"0x{0:02x}".format(deserialized))
def tests():
    """
    Function to test all int size-fixed values
    """
    cases = [(3, b'\x03\0\0\0', S4BLEInt),
             (3, b'\x03\0\0\0', U4BLEInt),
             (1000000, b'\x40\x42\x0f\0\0\0\0\0', U8BLEInt),
             (7, b'\x07\0\0\0\0\0\0\0', U8BLEInt),
             (0xF0, bytes().fromhex("f0"), VarInt),
             (0xF0F1, bytes().fromhex("fdf1f0"), VarInt),
             (0xFD, bytes().fromhex("fdfd00"), VarInt),
             (0xF0F1F2F3, bytes().fromhex("fef3f2f1f0"), VarInt),
             (0xF0F1F2F3F4F5F6F7, bytes().fromhex("fff7f6f5f4f3f2f1f0"), VarInt)
            ]

    print("Starting serialization test")
    for case in cases:
        print("Testing", case[2].__name__, "class.")
        serialize_tests(*case)

    print("Tests passed")
# Classes tests
if __name__ == "__main__":
    tests()
