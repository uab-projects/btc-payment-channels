"""
Transaction input
"""
from ..field.interfaces import Serializable
from ..tx import Tx


class TxInput(Serializable):
    """
    """
    __slots__ = ["_utxoID", "_utxoN", "_scriptLen", "_scriptSig", "_sequence"]

    def __init__(self):
        pass
