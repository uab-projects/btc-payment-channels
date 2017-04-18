"""
Models a Bitcoin scriptPubKey for the P2PKH payment method
"""
# Libraries
from .model import ScriptPubKey
from ... import address
from ...field.opcode import OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG
from ...field.script import StackDataField


class P2PKH(ScriptPubKey):
    """
    Creates a P2PKH scriptPubKey given a P2PKH address that will provide the
    public key hash, automatically creating the scriptPubKey.

    The public key hash value in the script will be invalid until a valid
    address is set. And after that, if the address object is modified, the
    public key hash value will be invalid until serialization
    """

    def __init__(self, new_address):
        """
        Initializes a P2PKH and creates the basic P2PKH, given the address
        containing the public key hash

        Args:
            new_address (address.P2PKH): p2pkh address to build pubkey script
            from
        """
        # Initialize super
        super().__init__(new_address)
        # Check address
        assert isinstance(new_address, address.P2PKH), """ address to set must
        be a P2PKH address object """
        # Build script
        self._build()

    def _build(self):
        """
        Creates the script with the opcodes of a P2PKH scriptPubKey
        """
        self._data.append(OP_DUP)
        self._data.append(OP_HASH160)
        self._data.append(StackDataField(self._address.public_key_hash))
        self._data.append(OP_EQUALVERIFY)
        self._data.append(OP_CHECKSIG)
