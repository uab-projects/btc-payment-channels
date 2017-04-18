"""
Defines ECDSA defaults
"""
# Libraries
# # App
from .secp256k1 import Secp256k1

# Constants
DEFAULT_CURVE = Secp256k1()
"""
    CurveParams: default ECDSA curve to use
"""
