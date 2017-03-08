# -*- coding: utf-8 -*-
"""
Defines Bitcoin transaction models.

In Bitcoin, a transaction is how funds are moved. The transaction specifies
one or more inputs to be spent and one or more outputs where the funds will
be moved if transaction is accepted as valid on the blockchain by consensus.

Transaction models must be able to represent transactions of the blockchain and
be able to be serialized into an array of bytes and deserialized from an array
of bytes

For more low-level detail about a transaction, check:
https://en.bitcoin.it/wiki/Transaction

Check also the implementation for Input and Output class for more information
about it
"""

# Libraries
from .interfaces import Serializable
from .field.general import S4BLEInt, U4BLEInt, VarInt

# Constants
DEFAULT_VERSION = 1
"""
int: Version of the Bitcoin protocol transaction, currently (2017-02-21)
just 1 is accepted as valid
"""
DEFAULT_INPUTS = None
DEFAULT_OUTPUTS = None
DEFAULT_LOCKTIME = 0
"""
int: Time (as number of blocks or as UNIX timestamp) at which transaction is
unlocked

¿DISABLED?

By default, will be zero as we want non-locked transactions by default

If lockTime < 500000000: specifies block number at which tx is unlocked
If locktime >= 500000000: specifies UNIX time stamp at which tx is unlocked

If all inputs have a sequence with 0xffffffff value, then this is ignored.
And as the feature of sequence is disabled, this is always 0
http://bitcoin.stackexchange.com/questions/2025/what-is-txins-sequence
"""


class Tx(Serializable):
    """
    Model of generic Bitcoin transaction, with a version field, inputs, outputs
    and locktime field

    Attributes:
        version (int): version of the transaction
        inputs (list): list of inputs (as Input objects) to be spent
        outputs (list): list of outputs (as Output objects) to be spent
        locktime (int): time when the transaction will be valid
    """
    __slots__ = ["_version", "_inputs", "_outputs", "_locktime"]

    def __init__(self, version=DEFAULT_VERSION, inputs=None, outputs=None,
                 locktime=DEFAULT_LOCKTIME):
        """
        Initializes a transaction with the specified version, inputs, outputs
        and locktime.

        Args:
            version (int): version of the transaction (default specified in
            params)
            inputs (list): list of inputs (as Input objects) to be spent
            outputs (list): list of outputs (as Output objects) to be spent
            locktime (int): time when the transaction will be valid
        """
        self._version = S4BLEInt(version)
        self._inputs = inputs if inputs is not None else []
        self._outputs = outputs if outputs is not None else []
        self._locktime = U4BLEInt(locktime)

    def serialize(self):
        """
        Serializes each field of the transaction and joins them into a single
        bytes object. Serialization of the transaction is according to the
        following specification (see field types to understand names)
         - version -> S4BLEInt
         - nInputs -> VarInt
         - inputs -> Concatenation of inputs serialization
                     See class Input for input serialization details
         - nOutputs -> VarInt
         - outputs -> Concatenation of outputs serialization
                      See class Output for output serialization details
         - locktime -> U4BLEInt
        Returns:
            bytes: object containing the byte representation of the transaction
        """
        serialization_items = []
        serialization_items.append(self._version)
        serialization_items.append(VarInt(len(self._inputs)))
        serialization_items += self._inputs
        serialization_items.append(VarInt(len(self._outputs)))
        serialization_items += self._outputs
        serialization_items.append(self._locktime)
        serialized_items = [x.serialize() for x in serialization_items]
        return b''.join(serialized_items)

    def deserialize(self, data):
        """
        Deserializes each field of the transaction and fills the transaction
        with the values obtained from the transaction bytes

        Triggers an exception if can't deserialize

        Args:
            data:   bytes object with transaction to deserialize

        Returns:
            the object itself, with the transaction loaded
        """
        offset = 0
        version = S4BLEInt().deserialize(data[offset:4])
        offset += 4
        number_of_inputs = VarInt().deserialize(data[offset:])
        offset += len(number_of_inputs)
        inputs = []
        for input_i in range(number_of_inputs.value):
            # Deserialize inputs
            pass
        number_of_outputs = VarInt().deserialize(data[offset:])
        offset += len(number_of_outputs)
        outputs = []
        for output_i in range(number_of_outputs.value):
            # Deserialize outputs
            pass
        locktime = U4BLEInt().deserialize(data[offset:offset+4])
        offset += 4
        if offset != len(data):
            raise ValueError("""Serialization finished, but there's still """
                             """data to handle. Offset is at byte %d""" %
                             offset)
        # Do assignations
        self._version = version
        self._inputs = inputs
        self._outputs = outputs
        self._locktime = locktime
        return self

    @property
    def version(self):
        """
        Returns the version of the transaction

        Returns:
            int: transaction version
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets a new version for the transaction

        Args:
            version (int): new transaction version
        """
        self._version.value = version

    @property
    def inputs(self):
        """
        Returns the inputs of the transaction as a list

        Returns:
            list: transaction inputs
        """
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        """
        Sets new inputs for the transaction

        Args:
            inputs (list): new transaction inputs (as a list)
        """
        self._inputs = inputs

    @property
    def outputs(self):
        """
        Returns the outputs of the transaction as a list

        Returns:
            list: transaction outputs
        """
        return self._outputs

    @outputs.setter
    def outputs(self, outputs):
        """
        Sets new outputs for the transaction

        Args:
            outputs (list): new transaction outputs (as a list)
        """
        self._outputs = outputs

    @property
    def locktime(self):
        """
        Returns the locktime of the transaction

        Returns:
            int: transaction locktime
        """
        return self._locktime

    @locktime.setter
    def locktime(self, locktime):
        """
        Sets a new locktime for the transaction

        Args:
            locktime (int): new transaction locktime
        """
        self._locktime.value = locktime

    def add_input(self, tx_input):
        """
        Adds a transaction input to the inputs list

        Args:
            tx_input(TxInput): input to add to the list
        """
        self._inputs.append(tx_input)
        tx_input.tx = self

    def add_output(self, tx_output):
        """
        Adds a transaction output to the outputs list

        Args:
            tx_output(TxOutput): output to add to the list
        """
        self._outputs.append(tx_output)

    def __str__(self):
        """
        Prints the transaction in a beautiful, printable way

        Returns:
            str: String containing a human-readable transaction
        """
        txt = "Tx Transaction\n"
        txt += " - version: %d\n" % self._version.value
        txt += " - numberOfInputs: %d\n" % len(self._inputs)
        txt += " - inputs:\n"
        txt += " - numberOfOutputs: %d\n" % len(self._outputs)
        txt += " - outputs:\n"
        txt += " - locktime: %d\n" % (self._locktime.value)
        return txt

    def __eq__(self, other):
        """
        Compares if two transactions are equal by serializing them

        Args:
            other (Tx): other transaction to compare to

        Returns:
            bool: true if both transactions are equal (same serialization)
        """
        return self.serialize() == other.serialize()


if __name__ == "__main__":
    print("Testing Tx class")
    print(" Creating empty transaction")
    T_EMPTYTX = Tx()
    print(" Serializing empty transaction")
    T_EMPTYTX_SER = T_EMPTYTX.serialize()
    print(" Result of serialization:", T_EMPTYTX_SER.hex())
    print(" Deserializing previous transaction")
    T_EMPTYTX_CPY = Tx().deserialize(T_EMPTYTX_SER)
    print(" Result of deserialization...",
          "pass" if T_EMPTYTX_CPY == T_EMPTYTX else "failed")
