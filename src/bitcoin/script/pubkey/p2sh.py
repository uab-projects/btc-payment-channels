"""
Models a Bitcoin scriptPubKey for the P2SH method
"""
# Libraries
from .model import ScriptPubKey
from ... import address
from ...field.opcode import OP_HASH160, OP_EQUAL
from ...field.script import ScriptData


class P2SH(ScriptPubKey):
    """
    Creates a P2SH scriptPubKey given a P2SH address that will provide the
    redeem script hash, automatically creating the scriptPubKey.
    """

    def __init__(self, new_address, tx_output=None):
        """
        Initializes an empty P2SH and creates the basic P2PKH, changing the
        address object to a P2SH address object.

        Args:
            new_address (address.P2SH): P2SH address of the pubkey script
            tx_output (TxOutput): transaction output the script belongs to
        """
        # Initialize super
        super().__init__(tx_output, None, new_address)
        # Ensure type
        self.address = new_address

    def _build(self):
        """
        Creates the script with the opcodes and data of a P2SH scriptPubKey
        """
        self._data = [
            OP_HASH160, ScriptData(self._address.script_hash), OP_EQUAL
        ]

    @property
    def address(self):
        """
        Returns the address the P2SH scriptPubKey is paying to
        """
        return self._address

    @address.setter
    def address(self, new_address):
        """
        Sets the new address to pay to
        """
        # Check is P2SH
        assert isinstance(new_address, address.P2SH), "Address to set in " + \
            "a P2SH scriptPubKey must be a P2SH address object"
        self._address = new_address
