"""
Models generic payment scripts, used in P2SH
"""
from .model import PayScript
from .multisig import MultiSig

__all__ = ["PayScript", "MultiSig"]
