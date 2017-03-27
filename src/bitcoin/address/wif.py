"""
Models a WIF (Wallet Import Format) address type, that contains a compressed /
uncompressed private ECDSA key

Information extracted from:
https://en.bitcoin.it/wiki/Wallet_import_format

Tests extracted from:
http://gobittest.appspot.com/PrivateKey
"""
from .model import Address
from .types import Types
from .helper import DOUBLESHA256_CHECKSUM_SIZE, doublesha256_checksum,\
    doublesha256_checksum_validate

# Constants
PREFIX_SIZE = 1
"""
    int: size in bytes of the WIF address prefixes
"""
PRIVATE_KEY_MIN_SIZE = 16
"""
    int: minimum private key size in bytes
"""
PRIVATE_KEY_MAX_SIZE = 64
"""
    int: maximum private key size in bytes
"""
CHECKSUM_SIZE = DOUBLESHA256_CHECKSUM_SIZE
"""
    int: size in bytes for the address suffix checksum
"""


# Methods
def validate_private_key(private_key):
    """
    Given a private key as a bytes object, check if it's valid and raises
    an exception if not

    Args:
        private_key (bytes): private key as bytes object
    """
    # Check size
    if len(private_key) < PRIVATE_KEY_MIN_SIZE\
       or len(private_key) > PRIVATE_KEY_MAX_SIZE:
        raise ValueError("""Unable to set a private key with length %d
        bytes. Private keys have to be between %d-%d bytes""" % (
            len(private_key), PRIVATE_KEY_MIN_SIZE, PRIVATE_KEY_MAX_SIZE))


# Classes
class WIF(Address):
    """
    WIF address address. Allows to serialize, deserialize, encode
    and decode WIF addresses to obtain and set ECDSA private keys in a portable
    format

    Internal _value field contains the private key and checksum
    """

    def __init__(self, addr_net, private_key):
        """
        Initializes a WIF address given the address network and the private
        key as a bytes object

        Args:
            addr_net (Network): network the address operates in
            private_key (bytes): private ECDSA key as bytes object
        """
        # Assert types
        assert isinstance(private_key, bytes), """Private key must be a bytes
        object"""
        # Initialize super classes
        super().__init__(Types.wif, addr_net)
        # Assign value
        validate_private_key(private_key)
        self._value = private_key + doublesha256_checksum(
            self._prefix + private_key)

    @classmethod
    def deserialize(cls, address):
        """
        Deserializes the given address as an array of bytes, guessing its
        prefix and saving its info, checking that the prefix type is WIF and
        after that, setting the ECDSA private key value

        Args:
            address (bytes): bytes object containing an address to deserialize

        Returns:
            self: the object with the updated values
        """
        # Basic deserialization
        addr_obj = Address.deserialize(address)
        # Type check
        if(addr_obj.type != Types.wif):
            raise ValueError("""The deserialized address is not a WIF
            address""")
        # Validate private key
        private_key = addr_obj._value[:-CHECKSUM_SIZE]
        validate_private_key(private_key)
        # Return new object
        return cls(addr_obj.network, private_key)

    @property
    def private_key(self):
        """ Extracts the private key from the address """
        return self._value[:-CHECKSUM_SIZE]

    @property
    def checksum(self):
        """ Returns the address checksum """
        return self.value[-CHECKSUM_SIZE:]
