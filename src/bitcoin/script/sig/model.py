"""
More information could be found in:
https://bitcoin.org/en/developer-guide#standard-transactions
"""
# Libraries
from ..general import Script


class ScriptSig(Script):
    """
    Defines a basic ScriptSig interface

    Attributes:
        _input (TxInput): input the script belongs to
    """
    __slots__ = ["_input"]

    def __init__(self, tx_input=None):
        """
        Initializes a script sig, optionally setting the input it belongs to

        Args:
            tx_input (TxInput): input it belongs to
        """
        super().__init__()
        self._input = tx_input
        if tx_input is not None:
            tx_input.script = self

    @property
    def input(self):
        """ Returns the input the script sig belongs to """
        return self._input
