"""
More information could be found in:
https://bitcoin.org/en/developer-guide#standard-transactions
"""
# Libraries
from ..general import Script


class ScriptSig(Script):
    """
    Defines a basic ScriptSig interface
    """
    def __init__(self):
        super().__init__()