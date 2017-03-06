"""
Defines the input part to be in the general transaction, that can contain one
or more of those inputs.

The low-level specification of the input is there:
https://en.bitcoin.it/wiki/Protocol_documentation#tx
"""
from ..field.interfaces import Serializable
from ..field.general import U4BLEInt, VarLEChar, VarInt


class TxInput(Serializable):
    """
    A basic input for a transaction

    Attributes:
        _utxoID (VarLEChar): the hash of the referenced transaction
        _utxoN (U4BLEInt): the index of the specific output in the transaction
        _scriptLen (VarInt): The length of the signature script
        _scriptSig (): 	Computational Script for confirming transaction
        authorization
        _sequence (U4BLEInt): Transaction version as defined by the sender
    """
    __slots__ = ["_utxoID", "_utxoN", "_scriptLen", "_scriptSig", "_sequence"]

    def __init__(self, utxoID, utxoN, sequence=4294967295):
        self._utxoID = VarLEChar(utxoID)
        self._utxoN = U4BLEInt(utxoN)
        self._sequence = U4BLEInt(sequence)

    def serialize(self):
        serialized = []
        # Add utxoID
        serialized.append(self._utxoID.serialize())
        # Add utxo index number
        serialized.append(self._utxoN.serialize())
        # Calculate the script length
        scriptlen = VarInt(len(self._scriptSig))
        # Add the script length
        serialized.append(scriptlen.serialize())
        # Add script
        serialized.append(self._scriptSig.serialize())
        # Add the sequence
        serialized.append(self._sequence.serialize())

        return b''.join(serialized)

    def deserialize(self, data):
        """
        Not implemented yet
        """
        pass
