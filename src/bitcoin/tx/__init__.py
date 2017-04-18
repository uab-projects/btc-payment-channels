"""
Models a Bitcoin transaction and gives methods to also calculate the
pseudo-transactions used for signing
"""
from .model import BasicTx
from .sign import SignableTx, HashTypes, DEFAULT_HASHTYPE
Tx = BasicTx

# Exports
__all__ = ["BasicTx", "SignableTx", "Tx", "HashTypes", "DEFAULT_HASHTYPE"]
