"""
Models a Bitcoin address and provides method to check and validate addresses
"""
from .model import Address
from .types import Types
from .p2pkh import P2PKH
from .p2sh import P2SH
from .wif import WIF

__all__ = ["Address", "P2PKH", "P2SH", "WIF", "Types"]
