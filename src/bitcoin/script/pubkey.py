"""
Models a Bitcoin scriptPubKey and defines methods to fill the script pubkey
according to the address sent, that will detect if it's a P2SH, P2PKH,...
"""
from .general import Script


class ScriptPubKey(Script):
    """
    Creates a scriptPubKey to set in a transaction output field. Given a
    Bitcoin address, decodes it and fills the scriptPubKey with the proper
    contents so the script is valid

    Attributes:
        _address (Address): address to generate the script according to
    """
    __slots__ = ["_address"]

    def __init__(self, address):
        # Switch address type
        pass

    @property
    def address(self):
        """ Returns the pubkey address """
        return self._address
