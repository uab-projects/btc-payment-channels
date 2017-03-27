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

    def __init__(self, script, btc=None, satoshis=None):
        """
        Initializes a TxOutput with a value and script

        Either a value in satoshis or in bitcoins must be provided, priorizing
        first the satoshis value if both are provided

        Args:
            script (ScriptPubKey): pubkey script of the output
            value (int): number of satoshis of the output
            btc (float): number of bitcoins of the output
        """
        # Type checks
        assert isinstance(script, ScriptPubKey), """The script of the output
        must be a ScriptPubKey object"""
        assert isinstance(btc, int) or isinstance(btc, float) or btc is None, \
            """Number of bitcoins must be an integer or a float value"""
        assert isinstance(satoshis, int) or satoshis is None, """Number of
        satoshis must be an integer value"""
        assert btc is not None or satoshis is not None, """Either a number of
        satoshis or bitcoins must be provided to create the output"""

        # Transform satoshis or bitcoins
        if btc is not None:
            satoshis = btc_to_satoshi(btc)

        # Set values
        self._value = U8BLEInt(satoshis)
        self._script = script

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

    @classmethod
    def deserialize(cls, data):
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
        out = ""
        out += "\t - value: %d BTC (%s)\n" % \
            (satoshi_to_btc(self._value.value), self._value.serialize().hex())
        out += "\t - [script_size]: %d (%s)\n" % \
            (len(self._script), VarInt(len(self._script)).serialize().hex())
        out += "\t - script: %s\n" % str(self._script)
        return out
