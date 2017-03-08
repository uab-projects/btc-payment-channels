"""
Defines the bitcoin currency units and equivalences and methods to handle them
"""
# Constants
BTC_PER_SATOSHI = 100000000
"""
    int: Number of satoshis in 1 BTC
"""


# Methods
def btc_to_satoshi(value):
    """
    Given a BTC value, transforms the value into satoshis and returns it
    """
    return int(value * BTC_PER_SATOSHI)


def satoshi_to_btc(value):
    """
    Given a satoshi value, transforms the value into BTC and returns it
    """
    return value / BTC_PER_SATOSHI
