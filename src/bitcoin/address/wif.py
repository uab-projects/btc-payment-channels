"""
Models a WIF (Wallet Import Format) address type, that contains a compressed /
uncompressed private ECDSA key

Information extracted from:
https://en.bitcoin.it/wiki/Wallet_import_format

Tests extracted from:
http://gobittest.appspot.com/PrivateKey
"""
# Libraries
# # App
from ..nets import DEFAULT_NETWORK
from .model import Address
from .types import Types
from ..crypto.ecdsa import private_to_public, validate_private_key
from ..crypto.hash import checksum

# Constants
PREFIX_SIZE = 1
"""
    int: size in bytes of the WIF address prefixes
"""
CHECKSUM_SIZE = 4
"""
    int: size in bytes for the address suffix checksum
"""
WIF_UNCOMPRESSED_SIZE = 32
"""
    int: normal WIF address size in bytes
    source:
    https://github.com/vbuterin/pybitcointools/blob/master/bitcoin/main.py
"""
WIF_COMPRESSED_SIZE = 33
"""
    int: compressed WIF address size in bytes
    source:
    https://github.com/vbuterin/pybitcointools/blob/master/bitcoin/main.py
"""
PRIVATE_COMPRESSED_SIZE = 32
"""
    int: normal private compressed size in bytes
    source:
    https://github.com/vbuterin/pybitcointools/blob/master/bitcoin/main.py
"""


# Classes
class WIF(Address):
    """
    WIF address address. Allows to serialize, deserialize, encode
    and decode WIF addresses to obtain and set ECDSA private keys in a portable
    format

    Internal _value field contains the private key and checksum
    """
    def __init__(self, private_key, addr_net=DEFAULT_NETWORK):
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
        self._value = private_key + checksum(self._prefix + private_key)

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
        assert addr_obj.type == Types.wif, """The deserialized address is not
        a WIF address"""
        # Validate private key
        private_key = addr_obj._value[:-CHECKSUM_SIZE]
        validate_private_key(private_key)
        # Return new object
        return cls(private_key, addr_net=addr_obj.network)

    @property
    def private_key(self):
        """
        Extracts the private key from the address

        Source:
        https://github.com/vbuterin/pybitcointools/blob/master/bitcoin/main.py
        """
        private_key = self._value[:-CHECKSUM_SIZE]
        if self.compressed:
            private_key = private_key[:PRIVATE_COMPRESSED_SIZE]
        return private_key

    @property
    def public_key(self):
        """ Extracts the public key from the private key contents """
        return private_to_public(self.private_key)

    @property
    def compressed(self):
        """ Calculates if the address is compressed or not """
        return len(self._value[:-CHECKSUM_SIZE]) == WIF_COMPRESSED_SIZE

    @property
    def checksum(self):
        """ Returns the address checksum """
        return self.value[-CHECKSUM_SIZE:]
