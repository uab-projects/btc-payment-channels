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

# Classes tests
if __name__ == "__main__":
    # Field interface
    print("Testing Field main interface")
    print(" Creating Field instance")
    T_FIELD = Field()
    print(" Assigning a value (3)")
    T_FIELD.value = 3
    print(" Returning the value:", T_FIELD.value)
    print(" Test passed")
    # Integers test
    print("Testing U4BLEInt (unsigned 4-byte integer) class")
    print(" Creating U4BLEInt instance")
    T_U4BLE = U4BLEInt()
    print(" Assigning a value (3)")
    T_U4BLE.value = 3
    print(" Returning the value:", T_U4BLE.value)
    print(" Serializing the value (as hex):", T_U4BLE.serialize().hex())
    print(" Deserializing the value:", T_U4BLE.deserialize(b'\x03\0\0\0').value)
    print(" Test passed")
    print("Testing S4BLEInt (signed 4-byte integer) class")
    print(" Creating S4BLEInt instance")
    T_S4BLE = S4BLEInt()
    print(" Assigning a value (3)")
    T_S4BLE.value = 3
    print(" Returning the value:", T_S4BLE.value)
    print(" Serializing the value (as hex):", T_S4BLE.serialize().hex())
    print(" Deserializing the value:", T_S4BLE.deserialize(b'\x03\0\0\0').value)
    print(" Test passed")
    #===========================================================================
    print("Testing U8BLEInt (signed 8-byte integer) class")
    print(" Creating U8BLEInt instance")
    T_U8BLE = U8BLEInt()
    print(" Assigning a value (1000000)")
    T_U8BLE.value = 1000000
    print(" Returning the value:", T_U8BLE.value)
    print(" Serializing the value (as hex):", T_U8BLE.serialize().hex())
    print(" Deserializing the value:",
          T_U8BLE.deserialize(b'\x40\x42\x0f\0\0\0\0\0').value)
    print(" Test passed")
    #===========================================================================
    print("Testing VarInt (variable-sized integer) class")
    print(" Creating VarInt instance")
    T_VARINT = VarInt()
    print(" Assigning a 1-byte encodable value")
    T_VARINT.value = 0xF0
    print(" Serializing the value", "0x{0:02x}".format(T_VARINT.value), "=",
          T_VARINT.serialize().hex())
    if len(T_VARINT.serialize()) != 1:
        raise ValueError(" Value", T_VARINT.value, "should fit in 1 byte!")
    print(" Assigning a 3-byte encodable (1-byte size + 2-byte int) value")
    T_VARINT.value = 0xF0F1
    print(" Serializing the value", "0x{0:02x}".format(T_VARINT.value), "=",
          T_VARINT.serialize().hex())
    if len(T_VARINT.serialize()) != 3:
        raise ValueError(" Value", T_VARINT.value, "should fit in 3 bytes!")
    print(" Tricky value 0xFD, should be encoded in 3 bytes")
    T_VARINT.value = 0xFD
    print(" Serializing the value", "0x{0:02x}".format(T_VARINT.value), "=",
          T_VARINT.serialize().hex())
    if len(T_VARINT.serialize()) != 3:
        raise ValueError(" Value", T_VARINT.value, "should fit in 3 bytes!")
    print(" Assigning a 5-byte encodable (1-byte size + 4-byte int) value")
    T_VARINT.value = 0xF0F1F2F3
    print(" Serializing the value", "0x{0:02x}".format(T_VARINT.value), "=",
          T_VARINT.serialize().hex())
    if len(T_VARINT.serialize()) != 5:
        raise ValueError(" Value", T_VARINT.value, "should fit in 5 bytes!")
    print(" Assigning a 9-byte encodable (1-byte size + 8-byte int) value")
    T_VARINT.value = 0xF0F1F2F3F4F5F6F7
    print(" Serializing the value", "0x{0:02x}".format(T_VARINT.value), "=",
          T_VARINT.serialize().hex())
    if len(T_VARINT.serialize()) != 9:
        raise ValueError(" Value", T_VARINT.value, "should fit in 9 bytes!")
    print("All serialize tests passed")
    # End of serializing tests
    print("Starting deseraliazing tests")
    print(" Creating a 1-byte decodable value")
    T_VARINT.deserialize((0xf0).to_bytes(1, byteorder='big'))
    print(" Deserializing a 1-byte value", "0x{0:02x}".format(0xf0), "=",
          "0x{0:02x}".format(T_VARINT.value))
    if T_VARINT.value != 0xf0:
        raise ValueError(" Value "+"0x{0:02x}".format(0xf0)+" != "+\
                         "0x{0:02x}".format(T_VARINT.value))
    print(" Creating a 3-byte decodable value")
    T_VARINT.deserialize((0xfdf1f0).to_bytes(3, byteorder='big'))
    print(" Deserializing a 3-byte value", "0x{0:02x}".format(0xfdf1f0), "=",
          "0x{0:02x}".format(T_VARINT.value))
    if T_VARINT.value != 0xf0f1:
        raise ValueError(" Value "+"0x{0:02x}".format(0xf0f0)+" != "+\
                         "0x{0:02x}".format(T_VARINT.value))
    print(" Creating a 5-byte decodable value")
    T_VARINT.deserialize((0xfef3f2f1f0).to_bytes(5, byteorder='big'))
    print(" Deserializing a 5-byte value", "0x{0:02x}".format(0xfef3f2f1f0),
          "=", "0x{0:02x}".format(T_VARINT.value))
    if T_VARINT.value != 0xF0F1F2F3:
        raise ValueError(" Value "+"0x{0:02x}".format(0xF0F1F2F3)+" != "+\
                         "0x{0:02x}".format(T_VARINT.value))
    print(" Creating a 9-byte decodable value")
    T_VARINT.deserialize((0xfff7f6f5f4f3f2f1f0).to_bytes(9, byteorder='big'))
    print(" Deserializing a 9-byte value",
          "0x{0:02x}".format(0xfff7f6f5f4f3f2f1f0), "=", "0x{0:02x}".format(T_VARINT.value))
    if T_VARINT.value != 0xf0f1f2f3f4f5f6f7:
        raise ValueError(" Value "+"0x{0:02x}".format(0xf0f1f2f3f4f5f6f7)+\
                         " != "+"0x{0:02x}".format(T_VARINT.value))
    print(" Test passed")
    print("Testing VarLEChar")
    T_TX_BE = bytes().fromhex("""21f10dbfb0ff49e2853629517fa176dc00d943f203aa"""
                              """e3511288a7dd89280ac2""")
    T_TX_LE = bytes().fromhex("""c20a2889dda7881251e3aa03f243d900dc76a17f5129"""
                              """3685e249ffb0bf0df121""")
    print(" Serializing a 32-byte array (txId)...")
    T_VARLECHAR_SER = VarLEChar(T_TX_BE).serialize()
    if T_VARLECHAR_SER != T_TX_LE:
        raise ValueError(" Value "+T_TX_LE.hex()+" != "+T_VARLECHAR_SER.hex())
    print(" Deserializing a 32-byte array (txId in a raw tx)...")
    T_VARLECHAR_DES = VarLEChar().deserialize(T_TX_LE)
    if T_VARLECHAR_DES.value != T_TX_BE:
        # pylint: disable=E1101
        raise ValueError(" Value "+T_TX_BE.hex()+" != "+\
        T_VARLECHAR_DES.value.hex())
