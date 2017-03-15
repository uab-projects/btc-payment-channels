"""
Defines a transaction output in a Bitcoin transaction
"""
# Libraries
from ...interfaces import Serializable
from ...field.general import U8BLEInt, VarInt
from ...script.pubkey import ScriptPubKey
from ...units import satoshi_to_btc, btc_to_satoshi


class TxOutput(Serializable):
    """
    Defines a TxOutput, whose value and script can be easily modified.

    Value can be set in Satoshis or bitcoins, using the proper properties, but
    the value will end in the transaction as Satoshis.

    Attributes:
        value (U8BLEInt): value in satoshis of the output
        script (ScriptPubKey): script to send the output funds to
    """
    __slots__ = ["_value", "_script"]

    def __init__(self):
        """
        Initializes an empty TxOutput with no value and empty script
        """
        self._value = U8BLEInt(0)
        self._script = ScriptPubKey()

    def serialize(self):
        """
        Serializes the output into an array of bytes, following the
        specification in:
        https://en.bitcoin.it/wiki/Protocol_documentation#tx
        """
        serializable = []
        serializable.append(self._value)
        serializable.append(VarInt(len(self._script)))
        serializable.append(self._script)
        serialized = [item.serialize() for item in serializable]
        return b''.join(serialized)

    def deserialize(self):
        """
        Deserializes an array of bytes that is supposed to represent an
        output
        """
        raise NotImplementedError(""" Not implemented yet """)

    @property
    def value(self):
        """ Returns the value of the output in Satoshis """
        return self._value.value

    @value.setter
    def value(self, satoshis):
        """ Sets the output value in Satoshis """
        self._value.value = satoshis

    @property
    def btc(self):
        """ Returns the output value in BTC """
        return satoshi_to_btc(self._value.value)

    @btc.setter
    def btc(self, btc):
        """ Sets the output value in BTC """
        self._value.value = btc_to_satoshi(btc)

    @property
    def script(self):
        """ Returns the script of the output """
        return self._script

    @script.setter
    def script(self, script):
        """ Sets the output script """
        self._script = script

    def __str__(self):
        """
        Prints the output in a useful, printable way

        Returns:
            str: String containing a hex output
        """
        return self.serialize().hex()
