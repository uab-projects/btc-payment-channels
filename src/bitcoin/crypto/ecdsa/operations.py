"""
Operations performable with ECDSA algorithm
"""
# Libraries
# # App
from .defaults import DEFAULT_CURVE
from .calculator import fast_multiply

# Constants
PRIVATE_KEY_MIN_SIZE = 16
"""
    int: minimum private key size in bytes
"""
PRIVATE_KEY_MAX_SIZE = 64
"""
    int: maximum private key size in bytes
"""


# Methods
def private_to_public(key):
    """
    Given an ECDSA private key, returns it corresponding public key

    Source:
    https://github.com/vbuterin/pybitcointools/blob/master/bitcoin/main.py

    Args:
        key (long): private ECDSA key as a long number
        If key is given as bytes, then will be returned as bytes, properly
        converting them. Big endian is assumed

    Returns:
        long: Corresponding public ECDSA key as a long number
        or bytes object if passed a bytes private key
    """
    # Convert to int?
    bytes_format = False
    if isinstance(key, bytes):
        key = int.from_bytes(key, "big")
        bytes_format = True
    assert isinstance(key, int), """private key to convert must be either an
    int or bytes object"""
    # Calculate public key
    public = fast_multiply(DEFAULT_CURVE.g, key)
    # Reconvert
    if bytes_format:
        public = b'\x04' + public[0].to_bytes(32, "big") + \
                 public[1].to_bytes(32, "big")
    # Return public key
    return public


def validate_private_key(private_key):
    """
    Given a private key as a bytes object, check if it's valid and raises
    an exception if not

    Args:
        private_key (bytes): private key as bytes object
    """
    # Check size
    assert len(private_key) >= PRIVATE_KEY_MIN_SIZE\
        and len(private_key) <= PRIVATE_KEY_MAX_SIZE,\
        """Unable to set a private key with length %d bytes. Private keys have
        to be between %d-%d bytes""" % (
            len(private_key), PRIVATE_KEY_MIN_SIZE, PRIVATE_KEY_MAX_SIZE)
