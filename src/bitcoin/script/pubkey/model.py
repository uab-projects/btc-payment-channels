"""
Models a Bitcoin scriptPubKey and defines methods to fill the script pubkey
according to the address sent, that will detect if it's a P2SH, P2PKH,...
"""
# Libraries
from abc import abstractmethod
from ..general import Script


class ScriptPubKey(Script):
    """
    Creates a scriptPubKey to set in a transaction output field. Given a
    Bitcoin address, decodes it and fills the scriptPubKey with the proper
    contents so the script is valid

    Attributes:
        _address (Address): address to generate the script according to
                            address type has to be P2SH or P2PKH
    """
    __slots__ = ["_address"]

    def __init__(self, address):
        """
        Initializes a scriptPubKey with an address

        Args:
            new_address (address.Address): address of the script
        """
        super().__init__()
        self._address = address

    @abstractmethod
    def _build(self):
        """
        Adds the opcodes and data necessary to create the script
        """
        pass

    @property
    def address(self):
        """ Returns the pubkey address """
        return self._address
