"""
Defines fields that can appear in a script, including OP_CODES from opcode
module.
"""
# Libraries
# pylint: disable=W0401,W0614,E1101
import math
from .model import Field
from .general import U2BLEInt, U4BLEInt
from .opcode import *
from .helper import bfh
from . import test

class StackDataField(Field):
    """
    A stack data field allows to include data in a script that has to be pushed
    to the stack, that will automatically include the push data OP_CODE
    required so the data is correctly pushed into the stack.

    Attributes:
        _value (bytes|Field): saved value must be either a bytes object or a
        Field object so that can be serialized
    """
    def serialize(self):
        """
        Serializes the data saved, including the operation to push the
        serialized data into the stack depending on the serialized data length

        The opcode to push the data depends on the data length:
        If data length in bytes is
            >= OP_PUSHDATA_MIN (0x01) and <= OP_PUSHDATA_MAX (0x4b)
        then serialization is:
            <number of data bytes to push><data to push>
        else:
            Calculate how much bytes does the size of the data to be pushed
            occupies (if we want to push 65535 bytes of data, then we require
            two bytes to express 65535 bytes -> ceil(log_2(65535)/8) = 2)

            Knowing the bytes that the length of the data takes to be expressed
            we have to use OP_PUSHDATA1,2,4 depending if the bytes of data to
            be pushed can be represented in 1, 2 or 4 bytes.

            After the opcode OP_PUSHDATA we've chosen, we add the size in bytes
            of the data as a little-endian unsigned integer
            https://en.bitcoin.it/wiki/Script
            http://bitcoin.stackexchange.com/questions/2285/script-op-pushdatas

        Returns:
            bytes: array of bytes so the data stored can be pushed into the
            stack, adding the opcodes necessary for that to happen
        """
        # Get data as bytes
        serialized_data = self._value if isinstance(self._value, bytes) else \
                          self._value.serialize()
        # Get data length
        serialized_data_length = len(serialized_data)
        bytes_length_size = math.ceil(serialized_data_length.bit_length()/8)

        # Generate OP_CODEs so the data is pushed
        pushdata_opcodes = None
        if serialized_data_length >= OP_PUSHDATA_MIN and \
           serialized_data_length <= OP_PUSHDATA_MAX:
            pushdata_opcodes = bytes([serialized_data_length])
        elif bytes_length_size < OP_PUSHDATA_MAX_BYTES:
            pushdata_opcode = None
            pushdata_size = None
            # Switch size of number of bytes and pack
            if bytes_length_size == 1:
                pushdata_opcode = OP_PUSHDATA1.serialize()
                pushdata_size = bytes([serialized_data_length])
            elif bytes_length_size == 2:
                pushdata_opcode = OP_PUSHDATA2.serialize()
                pushdata_size = U2BLEInt(serialized_data_length).serialize()
            elif bytes_length_size <= 4:
                pushdata_opcode = OP_PUSHDATA4.serialize()
                pushdata_size = U4BLEInt(serialized_data_length).serialize()
            else:
                raise ValueError("""Length size does not have an opcode to
                                    allow it to be pushed into the stack
                                    and fit""")

            # Create serialized opcodes to push data to stack
            pushdata_opcodes = pushdata_opcode + pushdata_size
        else:
            raise ValueError("""Data is too big to be pushed into the stack. No
            opcode exists to push that""")

        return pushdata_opcodes + serialized_data

    def deserialize(self, data):
        """
        Given a bytes object that is known to contain as first byte a push data
        operation, decodes the operation and extracts the data from the bytes
        object, storing it as a bytes object in the value of the field

        The length of the bytes object can be different from the length of the
        actual data. The method will just save the data that the opcode and
        opcode data if it's the case says. The rest of data will be ignored

        Raise:
            ValueError: no data push opcode is found
        """
        # Variables
        data_size = 0
        opcode = data[0]
        offset = 1 # the opcode to push data is not data

        # Check opcode
        if opcode >= OP_PUSHDATA_MIN and opcode <= OP_PUSHDATA_MAX:
            data_size = opcode
        else:
            # Check opcode that pushes size into stack
            if opcode == OP_PUSHDATA1.value:
                data_size = data[offset]
                offset += 1
            elif opcode == OP_PUSHDATA2.value:
                data_size = U2BLEInt().deserialize(data[offset:offset+2]).value
                offset += 2
            elif opcode == OP_PUSHDATA4.value:
                data_size = U4BLEInt().deserialize(data[offset:offset+4]).value
                offset += 4
            else:
                raise ValueError("""Data to deserialize has not an opcode to """
                                 """push data to the stack""")

        # Resolve data
        self._value = data[offset:data_size+offset]
        return self

# Module testing
if __name__ == "__main__":
    # Define test cases
    CASES = [
        (bfh("f0f1f2f3"), bfh("04f0f1f2f3"), StackDataField),
        (bfh("01"*0xff), OP_PUSHDATA1.serialize()+bfh("ff"+"01"*0xff),
         StackDataField),
        (bfh("02"*0xffff), OP_PUSHDATA2.serialize()+bfh("ffff"+"02"*0xffff),
         StackDataField),
        (bfh("04"*0xffffff), OP_PUSHDATA4.serialize()+bfh("ffffff00"+"04"*0xffffff),
         StackDataField)
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