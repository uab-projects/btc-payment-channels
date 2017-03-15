"""
Defines a class to model a P2PKH address, this means, adding extra methods to
validate the checksum when deserializing or decoding and properties to later
get the public key hash from the address using the data property
"""
# Libraries
from .model import AddressType
from .types import Types
from .helper import DOUBLESHA256_CHECKSUM_SIZE, doublesha256_checksum,\
    doublesha256_checksum_validate, ripemd160_sha256

# Constants
PREFIX_SIZE = 1
"""
    int: size in bytes of the P2PKH prefixes
"""
PKH_SIZE = 20
"""
    int: size in bytes of all public key hashes
"""
CHECKSUM_SIZE = DOUBLESHA256_CHECKSUM_SIZE
"""
    int: size in bytes for the address suffix checksum
"""
ADDRESS_SIZE = PREFIX_SIZE + PKH_SIZE + CHECKSUM_SIZE
"""
    int: size in byte of the P2PKH addresses
"""


# Classes
class P2PKH(AddressType):
    """
    Pay to public key hash address. Allows to serialize, deserialize, encode
    and decode P2PKH addresses so the public key hash can be easily set and
    got to generate / decode easily P2PKH addresses, as checksum calculations
    are performed automagically

    Internal _value field is not used, as serialization and deserialization
    methods calculate them when needed.

    Attributes:
        pkh (bytes): public key hash as an array of bytes
    """
    __slots__ = ["_pkh"]

    def __init__(self):
        """ Same as Address constructor, but setting correct type """
        super().__init__(Types.p2pkh)
        self._pkh = bytes()

    @classmethod
    def from_public_key(cls, pk):
        """
        Given a public key, returns a filled address with the public key hash
        calculated and properly set

        Args:
            pk (bytes): public key bytes

        Returns:
            P2PKH: P2PKH address instance containing the public key hash
        """
        pkh = ripemd160_sha256(pk)
        address = cls()
        address.pkh = pkh
        return address

    def deserialize(self, address):
        """
        Deserializes the given address as an array of bytes, guessing its
        prefix and saving its info, checking that the prefix type is P2PKH and
        after that, setting the public key hash value

        Args:
            address (bytes): bytes object containing an address to deserialize

        Returns:
            self: the object with the updated values
        """
        # Check size
        if len(address) != ADDRESS_SIZE:
            raise ValueError("""P2PKH Address %s size in bytes is not valid.
        All P2PKH addresses have %d bytes""" % (address.hex(), ADDRESS_SIZE))
        # Basic deserialization
        super().deserialize(address)
        # Set public key hash
        self._pkh = self._value[:-CHECKSUM_SIZE]
        return self

    @property
    def pkh(self):
        """ Extracts the public key hash from the address """
        return self._pkh

    @pkh.setter
    def pkh(self, pkh):
        """ Sets the address public key hash, updating address value """
        # Check size
        if len(pkh) != PKH_SIZE:
            raise ValueError("""Unable to set a public key hash with length %d
            bytes. Public key hash has to be %d bytes""" % (len(pkh),
                                                            PKH_SIZE))
        # Update values
        self._pkh = pkh

    @property
    def value(self):
        """ Returns the value by calculating the checksum and prepending public
        key hash """
        return self._pkh + doublesha256_checksum(self._prefix + self._pkh)

    @value.setter
    def value(self, value):
        """
        Given a value supposed to be the public key hash and checksum,
        checks that the checksum for the public key hash and current prefix is
        valid and sets the value.

        This means to set the public key hash and checksum at once
        """
        # Check size
        if len(value) != PKH_SIZE + CHECKSUM_SIZE:
            raise ValueError("""Value is expected to be public key hash and
            checksum. Given a bytes object with %d bytes. Needed %d""" % (
                len(value), PKH_SIZE + CHECKSUM_SIZE))
        # Get pkh and checksum
        pkh = value[:-CHECKSUM_SIZE]
        checksum = value[-CHECKSUM_SIZE:]
        # Test checksum
        doublesha256_checksum_validate(self._prefix + self._pkh, checksum)
        # Save
        self._value = value
        self._pkh = pkh

    @property
    def checksum(self):
        """ Returns the address checksum """
        return self.value[-CHECKSUM_SIZE:]
