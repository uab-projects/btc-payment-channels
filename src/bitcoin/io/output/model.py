"""
Defines a transaction output in a Bitcoin transaction
"""
# Libraries
# # App
from ..model import TxInputOutput
from ...field import U8BLEInt, VarInt
from ...units import satoshi_to_btc, btc_to_satoshi


class TxOutput(TxInputOutput):
    """
    Defines a TxOutput, whose value and script can be easily modified.

    Value can be set in Satoshis or bitcoins, using the proper properties, but
    the value will end in the transaction as Satoshis.

    Attributes:
        value (U8BLEInt): value in satoshis of the output
        script (ScriptPubKey): script to send the output funds to
    """
    __slots__ = ["_value"]

    def __init__(self, script=None, btc=None, satoshis=None, tx=None):
        """
        Initializes a TxOutput with a value and script

        Either a value in satoshis or in bitcoins must be provided, priorizing
        first the satoshis value if both are provided

        Args:
            script (ScriptPubKey): pubkey script of the output
            value (int): number of satoshis of the output
            btc (float): number of bitcoins of the output
            tx (BasicTx): transaction the output belongs to
        """
        # Type checks
        assert isinstance(btc, int) or isinstance(btc, float) \
            or btc is None, "Number of bitcoins must be an integer or a " + \
                            "float value"
        assert isinstance(satoshis, int) or satoshis is None, \
            "Number of satoshis must be an integer value"
        assert btc is not None or satoshis is not None, "Either a number " + \
            "of satoshis or bitcoins must be provided to create the output"

        # Transform satoshis or bitcoins
        if satoshis is None:
            satoshis = btc_to_satoshi(btc)

        # Positive amount
        assert satoshis > 0, "Number of satoshis / BTC must be positive"

        # Set values
        super().__init__(tx, script)
        self._value = U8BLEInt(satoshis)
        self._script = script

    def serialize(self):
        """
        Serializes the output into an array of bytes, following the
        specification in:
        https://en.bitcoin.it/wiki/Protocol_documentation#tx
        """
        serializable = []
        # Add output value
        serializable.append(self._value)
        # Add script length and script itself
        if self._script is not None:
            # Add script size and data
            serializable.append(VarInt(len(self._script)))
            serializable.append(self._script)
        else:
            serializable.append(VarInt(0))
        # Serialize
        return b''.join([item.serialize() for item in serializable])

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

    def __str__(self, space="", output_n=None):
        """
        Returns the output in a useful, printable way

        Returns:
            str: String containing a hex output
        """
        out = ""
        if output_n is not None:
            out += "%s// output %02d\n" % (space, output_n)
        out += "%svalue:        %s (%f BTC)\n" % \
            (space, self._value, satoshi_to_btc(self._value.value))
        out += "%sscriptSize:   %s\n" % (space, VarInt(len(self._script)))
        out += "%sscript:       %s\n" % (space, str(self._script))
        return out
