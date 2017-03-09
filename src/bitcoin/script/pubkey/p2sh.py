"""
Models a Bitcoin scriptPubKey for the P2SH method
"""
# Libraries
from .model import ScriptPubKey
from .. import address
from ..field.opcode import OP_HASH160, OP_EQUAL
from ..field.script import StackDataField


class P2SH(ScriptPubKey):
    """
    Creates a P2SH scriptPubKey given a P2SH address that will provide the
    redeem script hash, automatically creating the scriptPubKey.

    The redeem script hash value in the script will be invalid until a valid
    address is set. And after that, if the address object is modified, the
    redeem script value will be invalid until serialization
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
        self._data.append(OP_HASH160)
        self._data.append(StackDataField(self._address.script_hash))
        self._data.append(OP_EQUAL)

    def serialize(self):
        """
        Serializes the P2SH scriptPubKey, updating the script hash first
        """
        self._data[1].value = self._address.script_hash
        return super().serialize()

    @property
    def address(self):
        """ Returns the pubkey address """
        return self._address

    @address.setter
    def address(self, new_address):
        """ Sets the P2SH address and updates the script hash field of the
        script """
        assert isinstance(new_address, address.P2SH), """ address to set must
        be a P2SH address object """
        self._address = new_address
        self._data[1].value = self._address.script_hash
