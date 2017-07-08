"""
Models a Bitcoin scriptPubKey script
"""
# Libraries
# # Built-in
from abc import abstractmethod
# # App
from ..model import TxInputOutputScript


class ScriptPubKey(TxInputOutputScript):
    """
    Creates a scriptPubKey to set in a transaction output field. It contains
    a reference to the output the script is being included in.

    It also may contain a Bitcoin address, to which the script is paying to.
    Depending on the type of address, a specific ScriptPubKey will be used.
    Because of that, this is just an abstract, non-usable class

    Attributes:
        _tx_output (TxOutput): transaction output the script belongs to
        _address (Address): address to generate the script according to
                            address type has to be P2SH or P2PKH
    """
    __slots__ = ["_address"]

    def __init__(self, tx_output=None, data=None, address=None):
        """
        Initializes a scriptPubKey with the tx_output, address and data given

        Args:
            tx_output (TxOutput): output the script pubkey belongs to
            new_address (address.Address): address of the script
        """
        super().__init__(tx_output, data)
        self._address = address

    @abstractmethod
    def _build(self):
        """
        Creates the scriptPubKey to pay to the given address
        """
        pass

    @property
    def address(self):
        """
        Returns the address of the script
        """
        return self._address

    @property
    def output(self):
        """
        Returns the output the script sig belongs to
        """
        return self.parent

    @output.setter
    def output(self, new_output):
        """
        Sets the output the scriptSig belongs to
        """
        self.parent = new_output
