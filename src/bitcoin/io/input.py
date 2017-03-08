"""
Defines the input part to be in the general transaction, that can contain one
or more of those inputs.

The low-level specification of the input is there:
https://en.bitcoin.it/wiki/Protocol_documentation#tx
"""
from ..field.interfaces import Serializable
from ..field.general import U4BLEInt, VarLEChar, VarInt
from ..script.sig import ScriptSig


class TxInput(Serializable):
    """
    A basic input for a transaction

    Attributes:
        _utxo_id (VarLEChar): the hash of the referenced transaction
        _utxo_n (U4BLEInt): the index of the specific output in the transaction
        _script ():	Computational Script for confirming transaction
        authorization
        _sequence (U4BLEInt): Transaction version as defined by the sender
        _tx (Tx): Transaction where the current input belongs.
    """
    __slots__ = ["_utxo_id", "_utxo_n", "_script", "_sequence", "_tx"]

    def __init__(self, utxoID, utxoN, sequence=0xffffffff):
        self._utxo_id = VarLEChar(utxoID)
        self._utxo_n = U4BLEInt(utxoN)
        self._script = ScriptSig()
        self._sequence = U4BLEInt(sequence)

    def serialize(self):
        serialized = []
        # Add utxoID
        serialized.append(self._utxo_id.serialize())
        # Add utxo index number
        serialized.append(self._utxo_n.serialize())
        # Calculate the script length
        scriptlen = VarInt(len(self._scriptSig))
        # Add the script length
        serialized.append(scriptlen.serialize())
        # Add script
        serialized.append(self._script.serialize())
        # Add the sequence
        serialized.append(self._sequence.serialize())

        return b''.join(serialized)

    def deserialize(self, data):
        """
        Not implemented yet
        """
        pass

    @property
    def utxo_id(self):
        """ Returns the hash of the referenced transaction """
        return self._utxo_id

    @property
    def utxo_n(self):
        """ Returns the index of the specific output in the transaction """
        return self._utxo_n

    @property
    def script(self):
        """ Returns the scriptsig """
        return self._script

    @script.setter
    def script(self, script):
        """ Sets the script, received as an instance of ScriptSig Class """
        if isinstance(script, ScriptSig):
            self._script = script
        else:
            raise ValueError("""Expected a ScriptSig instance""")

    @property
    def sequence(self):
        """ Returns the Sequence value """
        return self._sequence

    @sequence.setter
    def sequence(self, value):
        """ Sets the sequence value """
        self._sequence = U4BLEInt(value)

    @property
    def tx(self):
        """ Returns the transaction where the input belongs"""
        return self._tx

    @tx.setter
    def tx(self, trans):
        """ Sets the transaction reference """
        self._tx = trans