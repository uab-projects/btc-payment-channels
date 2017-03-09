"""
Models a Bitcoin scriptPubKey and defines methods to fill the script pubkey
according to the address sent, that will detect if it's a P2SH, P2PKH,...
"""
# Libraries
from ..general import Script
from .. import address


class ScriptPubKey(Script):
    """
    Creates a scriptPubKey to set in a transaction output field. Given a
    Bitcoin address, decodes it and fills the scriptPubKey with the proper
    contents so the script is valid

    Attributes:
        _address (Address): address to generate the script according to
                            address has to be P2SH or P2PKH
    """
    __slots__ = ["_address"]

    def __init__(self):
        """
        Initializes an empty scriptPubKey with an empty address
        """
        self._address = address.Address()

    @property
    def address(self):
        """ Returns the pubkey address """
        return self._address
