"""
Models a Bitcoin scriptPubKey for the P2PKH payment method
"""
# Libraries
# # App
from .model import ScriptPubKey
from ... import address
from ...field.opcode import OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG
from ...field.script import ScriptData


class P2PKH(ScriptPubKey):
    """
    Creates a P2PKH scriptPubKey given a P2PKH address that will provide the
    public key hash, automatically creating the scriptPubKey.

    The public key hash value in the script will be invalid until a valid
    address is set. And after that, if the address object is modified, the
    public key hash value will be invalid until serialization
    """
    def __init__(self, new_address, tx_output=None):
        """
        Initializes a P2PKH and creates the basic P2PKH, given the address
        containing the public key hash

        Args:
            new_address (address.P2PKH): p2pkh address to build pubkey script
            from
            tx_output (TxOutput): the output the script belongs to
        """
        super().__init__(tx_output, None, new_address)
        # Ensure type
        self.address = new_address

    def _build(self):
        """
        Creates the script with the opcodes and data of a P2PKH scriptPubKey
        """
        self._data = [
            OP_DUP, OP_HASH160, ScriptData(self._address.public_key_hash),
            OP_EQUALVERIFY, OP_CHECKSIG
        ]

    @property
    def address(self):
        """
        Returns the address the P2PKH scriptPubKey is paying to
        """
        return self._address

    @address.setter
    def address(self, new_address):
        """
        Sets the new address to pay to
        """
        # Check is P2PKH
        assert isinstance(new_address, address.P2PKH), "Address to set in " + \
            "a P2PKH scriptPubKey must be a P2PKH address object"
        self._address = new_address
