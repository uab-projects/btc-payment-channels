"""
Defines the Bitcoin networks available
"""
from enum import Enum, unique


@unique
class Network(Enum):
    unknown = -1
    mainnet = 0
    testnet = 1
