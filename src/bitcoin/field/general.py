# -*- coding: utf-8 -*-
"""
Defines data fields used widely around the Bitcoin protocol standards

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
 - Char: any character or bytes-composed field
"""

# Libraries
# # Built-in
import struct

# # App
from .model import Field
from . import test
from .helper import bfh


# Integer types
class U2BLEInt(Field):
    """
    Defines a Bitcoin protocol unsigned 2-byte integer field
    """
    name = "Unsigned 2-byte integer little-endian field (uint16_t)"
    description = "16 bits without 2-complement sign"

    def __len__(self):
        return 2

    def serialize(self):
        return struct.pack('<H', self._value)

    @classmethod
    def deserialize(cls, v):
        return cls(struct.unpack('<H', v)[0])


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

    @classmethod
    def deserialize(cls, v):
        return cls(struct.unpack('<l', v)[0])


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

    @classmethod
    def deserialize(cls, v):
        return cls(struct.unpack('<L', v)[0])


class U8BLEInt(Field):
    """
    Defines a Bitcoin protocol unsigned 8-byte integer field
    """
    name = "Unsigned 8-byte integer little-endian field (uint64_t)"
    description = "64 bits without 2-complement sign"

    def serialize(self):
        return struct.pack('<Q', self._value)

    @classmethod
    def deserialize(cls, v):
        return cls(struct.unpack('<Q', v)[0])


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
        return 2**(first_byte - cls.BYTE_LIMIT) if first_byte > cls.BYTE_LIMIT\
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

    @classmethod
    def deserialize(cls, v):
        size = cls.translate_size(v[0])
        value = None
        if size == 0:
            value = v[0]
        elif size == 2:
            value = struct.unpack('<H', v[1:3])[0]
        elif size == 4:
            value = struct.unpack('<L', v[1:5])[0]
        elif size == 8:
            value = struct.unpack('<Q', v[1:9])[0]
        else:
            raise ValueError("""Length of the deserialize variable integer """
                             """must be 1, 3, 5 or 9 bytes""")
        return cls(value)


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

    @classmethod
    def deserialize(cls, v):
        rw_value = bytearray(v)
        rw_value.reverse()
        return cls(bytes(rw_value))

    def __str__(self):
        return "<%s:%s()>" % (self.serialize().hex(),
                              self.__class__.__name__)


# Classes tests
if __name__ == "__main__":
    # Define test case
    CASES = [
        (0xf0f1, bfh("f1f0"), U2BLEInt),
        (-0x11223344, bfh("BCCCDDEE"), S4BLEInt),
        (0xf0f1f2f3, bfh("f3f2f1f0"), U4BLEInt),
        (1000000, bfh("40420f0000000000"), U8BLEInt),
        (0xf0f1f2f3f4f5f6f7, bfh("f7f6f5f4f3f2f1f0"), U8BLEInt),
        (0xf0, bfh("f0"), VarInt),
        (0xf0f1, bfh("fdf1f0"), VarInt),
        (0xfD, bfh("fdfd00"), VarInt),
        (0xf0f1f2f3, bfh("fEf3f2f1f0"), VarInt),
        (0xf0f1f2f3f4f5f6f7, bfh("fff7f6f5f4f3f2f1f0"),
         VarInt),
        (bfh("""21f10dbfb0ff49e2853629517fa176dc00d943f203aae3511288a7dd8928"""
             """0ac2"""),
         bfh("""c20a2889dda7881251e3aa03f243d900dc76a17f51293685e249ffb0bf0d"""
             """f121"""), VarLEChar),
    ]
    # Run tests
    print("Starting serialization test")
    for case in CASES:
        print("-> Testing", case[2].__name__, "class.")
        print("      ", end='')
        test.serialization(*case)
        print("      ", end='')
        test.deserialization(*case)
    print("Tests passed")
