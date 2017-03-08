"""
Models a Bitcoin scriptPubKey and defines methods to fill the script pubkey
according to the address sent, that will detect if it's a P2SH, P2PKH,...
"""
# Libraries
from .general import Script
from .. import address
from ..field.opcode import OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG
from ..field.script import StackDataField


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


class P2PKH(Script):
    """
    Creates a P2PKH scriptPubKey given a P2PKH address that will provide the
    public key hash, automatically creating the scriptPubKey.

    The public key hash value in the script will be invalid until a valid
    address is set. And after that, if the address object is modified, the
    public key hash value will be invalid until serialization
    """

    def __init__(self):
        """
        Initializes an empty P2PKH and creates the basic P2PKH, changing the
        address object to a P2PKH address object
        """
        super().__init__()
        self._address = address.P2PKH()
        self._build()

    def _build(self):
        """
        Initializes the script with the opcodes of a P2PKH scriptPubKey
        """
        self._data.append(OP_DUP)
        self._data.append(OP_HASH160)
        self._data.append(StackDataField(self._address.pkh))
        self._data.append(OP_EQUALVERIFY)
        self._data.append(OP_CHECKSIG)

    def serialize(self):
        """
        Serializes the P2PKH scriptPubKey, updating the public key hash first
        """
        self._data[2].value = self._address.pkh
        return super().serialize()

    @property
    def address(self):
        """ Returns the pubkey address """
        return self._address

    @address.setter
    def address(self, new_address):
        """ Sets the pubkey address and updates the pkh field of the script """
        assert isinstance(new_address, address.P2PKH), """ address to set must
        be a P2PKH address object """
        self._address = new_address
        self._data[2].value = self._address.pkh
