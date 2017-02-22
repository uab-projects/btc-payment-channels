"""
Performs tests with base58.

Tests with encoding addresses, script hashes...
"""


from hashlib import sha256, new
from binascii import unhexlify, hexlify
from bitcoin.base58 import encode, decode


def HASHMD160(b):
    """
    Given some bytes, returns its RIPEMD160 hash.

    Args:
      - bytes: bytes to hash
    Returns:
      hash of the bytes
    """
    md = new('ripemd160')
    md.update(b)
    return md.hexdigest()


def OP_HASH160(b):
    """
    Given some bytes, returns its RIPEMD160(SHA256(bytes)) hash.

    Args:
     - bytes: bytes to hash
    Returns
     Hashed bytes
    """
    h = sha256(b).digest()
    return h


if __name__ == "__main__":
    val = "a980"
    ver = "00"
    print("HEX:                ", val)
    print("HEX-encoded:        ", unhexlify(val))
    print("OP_HASH160-encoded: ", OP_HASH160(unhexlify(val)))
    print("OP_HASH160-decoded: ", hexlify(OP_HASH160(unhexlify(val))))
    print("Add version:        ", unhexlify(ver)+OP_HASH160(unhexlify(val)))
    print("BTC Address:        ", encode(unhexlify(ver)+OP_HASH160(unhexlify(val))))
