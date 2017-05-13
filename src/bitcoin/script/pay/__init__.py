"""
Models generic payment scripts, used in P2SH
"""
from .model import PayScript
from .multisig import MultiSig
from .timed import TimeLockedScript

__all__ = ["PayScript", "MultiSig", "TimeLockedScript"]
