# -*- coding: utf-8 -*-
"""
Defines data fields used in transactions.

See model class for more information about naming
"""

# Libraries
import struct
from .model import Field

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

# Character classes
class VarLEChar(Field):
    """
    Defines a Bitcoin standard uchar[], encoded in little-endian
    """
    name = "Bitcoin variable-length unsigned little-endian character array"
    description = "Allows to save a variable-length character array in LE"
    def __len__(self):
        return len(self._value)
    def serialize(self):
        rw_value = bytearray(self._value)
        rw_value.reverse()
        return bytes(rw_value)
    def deserialize(self, v):
        rw_value = bytearray(v)
        rw_value.reverse()
        self._value = bytes(rw_value)
        return self

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
    if isinstance(deserialized, bytes):
        print(" Serializing the value", deserialized.hex())
    else:
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
             (0xF0F1F2F3F4F5F6F7, bytes().fromhex("fff7f6f5f4f3f2f1f0"),
              VarInt),
             (bytes().fromhex("""21f10dbfb0ff49e2853629517fa176dc00d943f203aa"""
                              """e3511288a7dd89280ac2"""),
              bytes().fromhex("""c20a2889dda7881251e3aa03f243d900dc76a17f5129"""
                              """3685e249ffb0bf0df121"""), VarLEChar),
            ]

    print("Starting serialization test")
    for case in cases:
        print("Testing", case[2].__name__, "class.")
        serialize_tests(*case)

    print("Tests passed")
# Classes tests
if __name__ == "__main__":
    tests()
