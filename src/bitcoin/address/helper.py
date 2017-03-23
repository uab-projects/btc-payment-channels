"""
Methods that ease computation of common values in addresses, like the checksum
"""
# Libraries
from hashlib import sha256, new
from . import prefix

# Constants
DOUBLESHA256_CHECKSUM_SIZE = 4
"""
    int: size of the checksums that are calculated with double sha256 hashing
"""


# Methods
def guess_prefix(address):
    """
    Given an address, tries to gets its prefix and therefore the type and
    network of it. If it succeeds, returns network, type and prefix, if not,
    raises an Exception.

    Args:
        address (bytes): address to guess prefix from

    Returns:
        tuple: network, type and prefix tuple

    Raises:
        ValueError: if prefix can't be guessed
    """
    # Guess type and network
    guess_info = prefix.guess(address)

    # Check if guessed
    if guess_info is None:
        raise ValueError("""The address (%s) is not related to any
        defined network or prefix for any network""" % (address.hex()))
    else:
        guess_network, guess_type = guess_info

    # Save values
    return guess_network, guess_type, \
        prefix.get(guess_network, guess_type.name)


def ripemd160_sha256(value):
    """
    Given a value in bytes, calculates its ripemd(sha256(value)) and
    returns it
    Args:
        value (bytes): bytes to calculate the checksum against

    Returns:
        bytes: 20-byte hash result
    """
    ripemd = new("ripemd160")
    ripemd.update(sha256(value).digest())
    return ripemd.digest()


def doublesha256(value):
    """
    Given a value in bytes, calculates its checksum and returns it

    Result is therefore:
        sha256(sha256(value))

    Args:
        value (bytes): bytes to calculate the checksum against

    Returns:
        bytes: double sha256 checksum
    """
    # Check checksum
    return sha256(sha256(value).digest()).digest()


def doublesha256_checksum(value):
    """
    Given a value in bytes, calculates its checksum and returns it, cutting the
    checksum according to common double sha256 bytes checksum used in address

    Checksum is therefore:
        sha256(sha256(value))[:4] (first four bytes of double sha256 hash)

    Args:
        value (bytes): bytes to calculate the checksum against

    Returns:
        bytes: 4-byte double sha256 checksum
    """
    # Check checksum
    return doublesha256(value)[:DOUBLESHA256_CHECKSUM_SIZE]


def doublesha256_checksum_validate(value, checksum):
    """
    Checks if the given value in bytes has the checksum passed, or raises an
    exception if not

    Args:
        value (bytes): bytes to calculate the checksum against
        checksum (bytes): supposed checksum

    Raises:
        ValueError: if checksum doesn't match calculated checksum
    """
    # Check checksum
    valid_checksum = doublesha256_checksum(value)
    if valid_checksum != checksum:
        raise ValueError("""Invalid checksum.
            Calculated checksum is %s, given is %s""" % (
                valid_checksum.hex(), checksum.hex()))
