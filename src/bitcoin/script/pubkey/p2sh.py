"""
Models a Bitcoin scriptPubKey for the P2SH method
"""
# Libraries
from .model import ScriptPubKey
from ... import address
from ...field.opcode import OP_HASH160, OP_EV
from ...field.script import StackDataField


class P2SH(ScriptPubKey):
    """
    Creates a P2SH scriptPubKey given a P2SH address that will provide the
    redeem script hash, automatically creating the scriptPubKey.
    """

    def __init__(self, new_address):
        """
        Initializes an empty P2SH and creates the basic P2PKH, changing the
        address object to a P2SH address object.

        Args:
            new_address (address.P2SH): P2SH address of the pubkey script
        """
        # Initialize super
        super().__init__(new_address)
        # Check address
        assert isinstance(new_address, address.P2SH), """ address to set must
        be a P2SH address object """
        # Build script
        self._build()

    def _build(self):
        """
        Creates the script with the opcodes of a P2SH scriptPubKey
        """
        self._data.append(OP_HASH160)
        self._data.append(StackDataField(self._address.script_hash))
        self._data.append(OP_EV)
