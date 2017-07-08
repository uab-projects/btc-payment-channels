"""
Models generic payment scripts, used in P2SH
"""
# Libraries
# # App
from .model import PayScript
from .multisig import MultiSig
from .timed import TimeLockedScript

# Exports
__all__ = ["PayScript", "MultiSig", "TimeLockedScript"]
