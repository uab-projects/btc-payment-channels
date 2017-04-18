"""
Models the parameters an ECDSA curve must contain
"""


class CurveParams(object):
    """
    Defines the parameters an ECDSA algorithm elliptic curve must define
    https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm

    Attributes:
        g (tuple): ellpitic curve base point, generator of the elliptic curve
                   with large prime order n, as a tuple of x, y longs
        n (long): integer order of G, means that n X G = 0
    """
    __slots__ = ["g", "n"]

    def __init__(self, g, n):
        """
        Initializes a basic curve with parameters G and N
        """
        self.n = n
        self.g = g
