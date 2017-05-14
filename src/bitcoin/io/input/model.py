"""
Defines the input part to be in the general transaction, that can contain one
or more of those inputs.

The low-level specification of the input is there:
https://en.bitcoin.it/wiki/Protocol_documentation#tx
"""
from ...interfaces import Serializable
from ...field.general import U4BLEInt, VarLEChar, VarInt
from ...script.sig import ScriptSig


class TxInput(Serializable):
    """
    A basic input for a transaction

    Attributes:
        _utxo_id (VarLEChar): the hash of the referenced transaction
        _utxo_n (U4BLEInt): the index of the specific output in the transaction
        _script (ScriptSig): scriptsig to spend the referred UTXO
        _sequence (U4BLEInt): Transaction version as defined by the sender
        _tx (Tx): Transaction where the current input belongs.
    """
    __slots__ = ["_utxo_id", "_utxo_n", "_script", "_sequence", "_tx"]

    def __init__(self, utxo_id, utxo_n, script=None, sequence=0xffffffff):
        """
        Initializes a transaction input given its UTXO id and number, the
        spending scriptsig and the optional sequence number

        Args:
            utxo_id (bytes): id of the transaction containing an UTXO
            utxo_n (int): number of output where the UTXO is located
            script (ScriptSig): scriptsig to spend the funds
            sequence (int): sequence number
        """
        self._utxo_id = VarLEChar(utxo_id)
        self._utxo_n = U4BLEInt(utxo_n)
        self._script = ScriptSig()
        # Given script
        if script is not None:
            self._script = script
            # Set the input
            if isinstance(script, ScriptSig):
                script._input = self
        self._sequence = U4BLEInt(sequence)

    def serialize(self):
        serialized = []
        # Add utxoID
        serialized.append(self._utxo_id.serialize())
        # Add utxo index number
        serialized.append(self._utxo_n.serialize())
        # Add the script length
        serialized.append(VarInt(len(self._script)).serialize())
        # Add script
        serialized.append(self._script.serialize())
        # Add the sequence
        serialized.append(self._sequence.serialize())

        return b''.join(serialized)

    @classmethod
    def deserialize(cls, data):
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
        self._script = script

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

    def __str__(self, space="", input_n=None):
        """
        Prints the input in a useful, printable way

        Returns:
            str: String containing a hex input
        """
        inp = ""
        if input_n is not None:
            inp += "%s// input %02d\n" % (space, input_n)
        inp += "%spreviousTx:   %s\n" % (space, self._utxo_id)
        inp += "%soutputNum:    %s\n" % (space, self._utxo_n)
        inp += "%sscriptSize:   %s\n" % (space, VarInt(len(self._script)))
        inp += "%sscript:       %s\n" % (space, self._script.__str__(
            space+"    "))
        inp += "%ssequence:     %s\n" % (space, self._sequence)
        return inp
