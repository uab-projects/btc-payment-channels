"""
Defines the hashcodes types existing
"""
# Libraries
from enum import Enum, unique


@unique
class Types(Enum):
    """
    Defines the types signature hash can be
    """
    unknown = -1
    sighash_all = 1
    sighash_none = 2
    sighash_single = 3
