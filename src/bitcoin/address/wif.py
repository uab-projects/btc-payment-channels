"""
Models a WIF (Wallet Import Format) address type, that contains a compressed /
uncompressed private ECDSA key

Information extracted from:
https://en.bitcoin.it/wiki/Wallet_import_format

Tests extracted from:
http://gobittest.appspot.com/PrivateKey
"""
from .model import AddressType
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


# Classes
class WIF(AddressType):
    """
    WIF address address. Allows to serialize, deserialize, encode
    and decode WIF addresses to obtain and set ECDSA private keys in a portable
    format

    Internal _value field is not used, as serialization and deserialization
    methods calculate them when needed.

    Attributes:
        _private_key (bytes): ECDSA private key the address contains
    """
    __slots__ = ["_private_key"]

    def __init__(self):
        """ Same as Address constructor, but setting correct type """
        super().__init__(Types.wif)
        self._private_key = bytes()

    def deserialize(self, address):
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
        super().deserialize(address)
        # Set private key
        self._private_key = self._value[:-CHECKSUM_SIZE]
        return self

    @property
    def private_key(self):
        """ Extracts the private key from the address """
        return self._private_key

    @private_key.setter
    def private_key(self, private_key):
        """ Sets the address ECSA private key, updating address value """
        # Check size
        if len(private_key) < PRIVATE_KEY_MIN_SIZE\
           or len(private_key) > PRIVATE_KEY_MAX_SIZE:
            raise ValueError("""Unable to set a private key with length %d
            bytes. Private keys have to be between %d-%d bytes""" % (
                len(private_key), PRIVATE_KEY_MIN_SIZE, PRIVATE_KEY_MAX_SIZE))
        # Update values
        self._private_key = private_key

    @property
    def value(self):
        """ Returns the value by calculating the checksum and prepending the
        private key """
        return self._private_key + doublesha256_checksum(
            self._prefix + self._private_key)

    @value.setter
    def value(self, value):
        """
        Given a value supposed to be the private key and checksum,
        checks that the checksum for the private key and current prefix is
        valid and sets the value.

        This means to set the private key and checksum at once
        """
        # Get private key and checksum
        private_key = value[:-CHECKSUM_SIZE]
        checksum = value[-CHECKSUM_SIZE:]
        # Test checksum
        doublesha256_checksum_validate(self._prefix + private_key, checksum)
        # Save
        self._value = value
        self._private_key = private_key

    @property
    def checksum(self):
        """ Returns the address checksum """
        return self.value[-CHECKSUM_SIZE:]
