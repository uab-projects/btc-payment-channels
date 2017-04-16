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
    """
    __slots__ = ["_sigNeeded", "_sigTotal", "_pubKeys"]

    def __init__(self, needed, total):
        self._sigNeeded = needed
        self._sigTotal = total
        self._pubKeys = []

    def add_PubKey(self, pubkey):
        """
        Adds a pubkey to the addressess list in order to have one more
        address to allow the payment

        Args:
            pubkey (): PubKey to append to the list of PubKey
        """
        assert len(self._pubKeys) < self._sigTotal, "Too many addressess"
        self._pubKeys.append(pubkey)

    def remove_PubKey(self, pubkey):
        """
        Removes a pubkey to the addressess list

        Args:
            pubkey (): PubKey to remove of the list of PubKey
        """
        assert pubkey in self._pubKeys, "Pubkey not in list"
        self._pubKeys.remove(pubkey)

    def _build(self):
        """
        Initializes the script with the opcodes and the data necessary.
        """
        # OP_M <pk_n> .. <pk_1> OP_N OP_CMS
        assert len(self._pubKeys) == self._sigTotal, """That scripts needs
        exactly %d pubkeys""" % self._sigTotal
        self._data.append(get_op_code_n(self._sigNeeded))
        for pk in self._pubKeys:
            self._data.append(StackDataField(pk))
        self._data.append(get_op_code_n(self._sigTotal))
        self._data.append(OP_CMS)

    @property
    def pay_script(self):
        return pay.MultiSig(self)


"""
RAW IDEA
ExpiringMultisig

    MultiSig(2,2) >>
        def _build(self):
            # self._data.append(OP_OVER)
            # Normal script
            super()._build()
            self._data +=
            [OP_NOTIF, <time>, OP_CLTV, OP_DROP, <pubkey>, OP_CS, OP_ENDIF]
"""
