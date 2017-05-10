"""
Models a ReedemScript for a multisignature Address
"""

from .. import pay
from .model import RedeemScript
from .helper import get_op_code_n
from ...field.opcode import OP_CMS
from ...field.script import StackDataField


class MultiSig(RedeemScript):
    """
    Models a Multisignature script

    Attributes:
        _keys_needed (int): number of keys needed to unlock the script funds
        _keys_total (int): number of keys in the multisig script
    """
    __slots__ = ["_keys_needed", "_keys_total", "_public_keys"]

    def __init__(self, needed, total=None):
        super().__init__()
        self._keys_needed = needed
        self._keys_total = total if total is not None else needed
        self._public_keys = []

    def add_public_key(self, public_key):
        """
        Adds a public key to the addressess list in order to have one more
        address to allow the payment

        Args:
            public_key (bytes): public key to append to the list of public keys
        """
        assert len(self._public_keys) < self._keys_total, "Too many addressess"
        self._public_keys.append(public_key)

    def remove_public_key(self, public_key):
        """
        Removes a public key from the addresses list

        Args:
            public_key (bytes): public key to remove of the list of public keys
        """
        assert public_key in self._public_keys, "Pubkey not in list"
        self._public_keys.remove(public_key)

    def _build(self):
        """
        Initializes the script with the opcodes and the data necessary.
        """
        # OP_M <pk_n> .. <pk_1> OP_N OP_CMS
        assert len(self._public_keys) == self._keys_total, """That scripts needs
        exactly %d pubkeys""" % self._keys_total
        self._data.append(get_op_code_n(self._keys_needed))
        for pk in self._public_keys:
            self._data.append(StackDataField(pk))
        self._data.append(get_op_code_n(self._keys_total))
        self._data.append(OP_CMS)

    @property
    def pay_script(self):
        return pay.MultiSig(self)
