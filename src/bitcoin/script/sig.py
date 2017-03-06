"""
"""
from .general import Script
from ..io.input import TxInput


class ScriptSig(Script):
    """
    """
    __slots__ = ["_input"]

    def __init__(self):
        super().__init__()

    def sign(self, privKey):
        """
        Description

        Args:
            privKey(Address): private key that will be used to sign the current
            transaction, that signature will be part of the transaction and the
            script.
        """
        pass
