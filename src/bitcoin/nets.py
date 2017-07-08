"""
Defines the Bitcoin networks available as constants to agree around the
module
"""
from enum import Enum, unique


# Classes
@unique
class Network(Enum):
    unknown = -1
    mainnet = 0
    testnet = 1


# Constants
DEFAULT_NETWORK = Network.testnet
"""
    Network.item: specifies the default network to use if no network is
    specified
"""
