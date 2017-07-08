"""
Models a Bitcoin transaction and gives methods to also calculate the
pseudo-transactions used for signing
"""
# Libraries
# # Apps
from .model import BasicTx
from .sign import SignableTx, HashTypes, DEFAULT_HASHTYPE

# Constants
Tx = BasicTx  # Because of 'legacy' issues

# Exports
__all__ = ["BasicTx", "SignableTx", "Tx", "HashTypes", "DEFAULT_HASHTYPE"]
