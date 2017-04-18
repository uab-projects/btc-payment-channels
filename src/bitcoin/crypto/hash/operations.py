"""
Defines commonly used hash operations around Bitcoin

All the methods here are supposed to receive and return bytes objects
"""
# Libraries
# # Built-in
import hashlib

# Constants
RIPEMD160 = "ripemd160"
"""
    str: string to look for RIPEMD160 algorithm in Python's hashlib library
"""
CHECKSUM_SIZE = 4
"""
    int: default number of bytes to cut when calculating checksum
"""
CHECKSUM_FIRST = True
"""
    bool: controls if by default the checksum are the first
    CHECKSUM_SIZE bytes or the latest ones
"""


# Methods
def ripemd160(value):
    """
    Given a value in bytes, calculates its ripemd(value) and
    returns it

    Args:
        value (bytes): bytes to calculate the checksum against

    Returns:
        bytes: 20-byte hash result
    """
    ripemd = hashlib.new(RIPEMD160)
    ripemd.update(value)
    return ripemd.digest()


def sha256(value):
    """
    Given a value in bytes, calculates its ripemd(value) and
    returns it

    Args:
        value (bytes): bytes to calculate the checksum against

    Returns:
        bytes: 20-byte hash result
    """
    return hashlib.sha256(value).digest()


def ripemd160_sha256(value):
    """
    Given a value in bytes, calculates its ripemd(sha256(value)) and
    returns it

    Args:
        value (bytes): bytes to calculate the checksum against

    Returns:
        bytes: 20-byte hash result
    """
    return ripemd160(sha256(value))


def double_sha256(value):
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
    return sha256(sha256(value))


# Some more constants
CHECKSUM_FUNC = double_sha256
"""
    function: default checksum function
"""


def checksum(value, func=double_sha256, size=CHECKSUM_SIZE,
             first=CHECKSUM_FIRST):
    """
    Given a value calculates its checksum. It allows to specify the checksum
    function, if the first or latest bytes must be taken and how many checksum
    bytes have to be taken. Defaults will be used if no value is specified

    Args:
        value (bytes): value to calculate checksum on
        func (function): function to use to generate the checksum hash
        size (int): size in bytes of the checksum
        first (bool): true to take n first bytes, false to take last
    """
    return func(value)[:size] if first else func(value)[-size:]


def checksum_validate(value, given_checksum, *args, **kwargs):
    """
    Checks if the given value in bytes has the checksum passed, or raises an
    exception if not. The checksum calculation parameters can be passed too

    Args:
        value (bytes): bytes to calculate the checksum against
        given_checksum (bytes): supposed checksum
        *args, **kwargs: extra arguments for checksum calculation

    Raises:
        ValueError: if checksum doesn't match calculated checksum
    """
    # Check checksum
    valid_checksum = checksum(value, *args, **kwargs)
    if valid_checksum != given_checksum:
        raise ValueError("""Invalid checksum.
            Calculated checksum is %s, given is %s""" % (
                valid_checksum.hex(), given_checksum.hex()))
