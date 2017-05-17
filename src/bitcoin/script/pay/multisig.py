"""
Models the operations needed to spend a MultiSig redeem script, that basically
are operations to add signatures
"""
# Library
from .model import PayScript
from ...field.opcode import OP_0
from ...field.script import ScriptData


class MultiSig(PayScript):
    """
    Allows to pay to a multisig redeem script by providing methods to add
    signatures and then serialize them (properly ordered)

    Attributes:
        _signatures (list): list of bytes object containing ECDSA signatures
                            that allow to spend a P2SH with a multisig redeem
                            script
    """
    __slots__ = ["_signatures"]

    def __init__(self, redeem):
        """
        Initializes a multisig pay script given the multisig redeem script
        we are paying to in order to perform some checks
        """
        super().__init__(redeem)
        self._signatures = []

    def add_signature(self, signature):
        """
        Adds a signature to the payment script

        Args:
            signature (bytes): signature to append to the list of signatures
        """
        self._signatures.append(signature)

    def _build(self):
        """
        Creates the list of signatures to be pushed into the stack
        """
        # Initialize
        self._data = []
        # OP_0 bug
        # We need to add it because of a off-by-one mistake
        # https://bitcoin.org/en/developer-guide#multisig
        self._data.append(OP_0)
        # Add signatures
        for sign in self._signatures:
            self._data.append(ScriptData(sign))
