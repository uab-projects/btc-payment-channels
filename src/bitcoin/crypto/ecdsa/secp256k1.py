"""
Contains constants for the secp256k1 curve

Sources:
https://en.bitcoin.it/wiki/Secp256k1
https://github.com/vbuterin/pybitcointools/blob/master/bitcoin/main.py
"""
# Libraries
# # App
from .curve import CurveParams

# Constants
P = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 2**0
A = 0
B = 7
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
G = (Gx, Gy)
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
H = 1


# Classes
class Secp256k1(CurveParams):
    """
    Defines a Secp256k1 ECDSA Koblitz curve params used in Bitcoin
    """
    __slots__ = ["p", "a", "b", "g", "n", "h"]

    def __init__(self):
        """ Initializes a secp256k1 curve parameters object """
        super().__init__(G, N)
        self.p = P
        self.a = A
        self.b = B
        self.h = H


# Objects
PARAMS = Secp256k1()
