"""
Models a ReedemScript for a multisignature Address
"""
# Libraries
# # Built-in
from .. import pay
from .model import RedeemScript
from ...field import OP_CMS, ScriptData, get_op_code_n


class MultiSig(RedeemScript):
    """
    Models a Multisignature script

    Attributes:
        _keys_needed (int): number of keys needed to unlock the script funds
            if no keys needed specified, the resulting script will have no
            needed keys specified, meaning that can be used for
            TimeLockedScripts, for example
        _keys_total (int): number of keys in the multisig script
            if not specified, will be the same as keys_needed
            if neither keys needed are specified or total keys, an error will
            be triggered
    """
    __slots__ = ["_keys_needed", "_keys_total", "_public_keys"]

    def __init__(self, needed=None, total=None):
        super().__init__(None)
        assert needed is not None or total is not None, "You must specify " + \
            "at least the needed keys or the total keys"
        self._keys_needed = needed
        self._keys_total = total if total is not None else needed
        self._public_keys = []

    def add_public_key(self, public_key):
        """
        Adds a public key to t he addressess list in order to have one more
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
        Creates the script with the opcodes and the data necessary:
            OP_M <pk_n> .. <pk_1> OP_N OP_CMS
        """
        # Check all keys are provided
        assert len(self._public_keys) == self._keys_total, "The MultiSig " + \
            "redeem script needs exactly %d pubkeys" % self._keys_total
        # Initialize and build
        self._data = []
        # Add needed keys to unlock
        if self._keys_needed is not None:
            self._data.append(get_op_code_n(self._keys_needed))
        # Add public keys
        for pk in self._public_keys:
            self._data.append(ScriptData(pk))
        # Add total number of public keys
        self._data.append(get_op_code_n(self._keys_total))
        # Checkmultisig
        self._data.append(OP_CMS)

    @property
    def pay_script(self):
        return pay.MultiSig(self)
