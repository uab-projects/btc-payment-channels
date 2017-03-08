"""
Defines transactions outputs models, factories and tests
"""
from .factory import p2pkh
from .model import TxOutput

__all__ = ["TxOutput", "p2pkh"]
