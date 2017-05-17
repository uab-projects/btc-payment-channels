"""
Defines the existing address types
"""
# Libraries
# # Built-in
from enum import Enum, unique


@unique
class Types(Enum):
    """
    Defines the types a Bitcoin address can be
    """
    unknown = -1
    p2pkh = 1
    p2sh = 2
    wif = 3
    bip32_pubkey = 4
    bip32_pkey = 5
