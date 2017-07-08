"""
Defines the input part to be in the general transaction, that can contain one
or more of those inputs.

The low-level specification of the input is there:
https://en.bitcoin.it/wiki/Protocol_documentation#tx
"""
# Libraries
# # App
from ..model import TxInputOutput
from ...field import U4BLEInt, VarLEChar, VarInt

# Constants
DEFAULT_SEQUENCE = 0xffffffff
"""
    int: default sequence number for inputs. Final value
"""


class TxInput(TxInputOutput):
    """
    Models a transaction input, containing the UTXO reference (aka outpoint),
    script and sequence number

    Attributes:
        _utxo_id (VarLEChar): the hash of the referenced transaction
        _utxo_n (U4BLEInt): the index of the specific output in the transaction
        _script (ScriptSig): scriptsig to spend the referred UTXO
        _sequence (U4BLEInt): Transaction version as defined by the sender
        _tx (Tx): Transaction where the current input belongs.
    """
    __slots__ = ["_utxo_id", "_utxo_n", "_script", "_sequence", "_tx"]

    def __init__(self, utxo_id, utxo_n, script=None,
                 sequence=DEFAULT_SEQUENCE, tx=None):
        """
        Initializes a transaction input given its UTXO id and number, the
        spending scriptsig and the optional sequence number

        Args:
            utxo_id (bytes): id of the transaction containing an UTXO
            utxo_n (int): number of output where the UTXO is located
            script (ScriptSig): scriptsig to spend the funds
            sequence (int): sequence number
            tx (BasicTx): transaction the output belongs to
        """
        super().__init__(tx, script)
        self._utxo_id = VarLEChar(utxo_id)
        self._utxo_n = U4BLEInt(utxo_n)
        self._sequence = U4BLEInt(sequence)

    def serialize(self):
        """
        Serializes the transaction input into a bytes object
        """
        serializable = []
        # Add utxo reference
        serializable.append(self._utxo_id)
        # Add utxo index number
        serializable.append(self._utxo_n)
        # Add the script length and script itself
        if self._script is not None:
            # Add script length and script
            serializable.append(VarInt(len(self._script)))
            serializable.append(self._script)
        else:
            # No script
            serializable.append(VarInt(0))
        # Add the sequence
        serializable.append(self._sequence)

        return b''.join([x.serialize() for x in serializable])

    @classmethod
    def deserialize(cls, data):
        """
        Not implemented yet
        """
        raise NotImplementedError("Pending to implement")

    @property
    def utxo_id(self):
        """
        Returns the hash of the referenced transaction
        """
        return self._utxo_id

    @property
    def utxo_n(self):
        """
        Returns the index of the specific output in the transaction
        """
        return self._utxo_n

    @property
    def sequence(self):
        """ Returns the Sequence value """
        return self._sequence

    @sequence.setter
    def sequence(self, value):
        """ Sets the sequence value """
        self._sequence = U4BLEInt(value)

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
