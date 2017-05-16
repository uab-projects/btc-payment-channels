"""
Defines basic data-structures for Bitcoin in Python, hard-coded parameters in
order to fill those data-structures and methods to serialize and deserialize
all of them in order to create valid data for the Bitcoin cryptocurrency
protocol

The aim of this module is to provide a puzzle-friendly framework to compose
easily any Bitcoin transaction, specially tohse containing smart contracts
"""
# Libraries
# # Parameters
from .nets import Network, DEFAULT_NETWORK
from .units import BTC_PER_SATOSHI, btc_to_satoshi, satoshi_to_btc
# # Addresses
from .address import Address, P2PKH as P2PKHAddress, P2SH as P2SHAddress, \
                     WIF as WIFAddress, Types as AddressTypes
# # Transactions
from .tx import SignableTx, BasicTx

# Exported items
__all__ = ["Network", "DEFAULT_NETWORK", "BTC_PER_SATOSHI", "btc_to_satoshi",
           "satoshi_to_btc", "Address", "P2PKHAddress", "P2SHAddress",
           "WIFAddress", "AddressTypes", "SignableTx", "BasicTx"]
