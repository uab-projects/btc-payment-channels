"""
More information could be found in:
https://bitcoin.org/en/developer-guide#standard-transactions
"""
from .general import Script
from ..field.script import StackDataField


class ScriptSig(Script):
    """
    """
    def __init__(self):
        super().__init__()


class P2PKH(ScriptSig):
    __slots__ = ["_address", "_input"]

    def __init__(self, address):
        self._address = address
        self._build()

    def _build(self):
        # Signature
        self._data.append(StackDataField())
        # PubKey
        self._data.append(StackDataField())


class P2SH(ScriptSig):
    """
    """
    __slots__ = ["_reedemScript"]

    def __init__(self, reedemScript):
        self._reedemScript = reedemScript
        self._build()

    def _build(self):
        # Signature(s)
        while 1:
            self._data.append(StackDataField())
        self._data.append(StackDataField(self._reedemScript))
