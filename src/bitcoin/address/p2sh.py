"""
Defines a class to model a P2SH address, this means, adding extra methods to
set the reedem script and generate the address automatically
"""
# Libraries
from .model import AddressType
from .types import Types

# Constants
PREFIX_SIZE = 1
"""
    int: size in bytes of the P2SH prefixes
"""
SH_SIZE = 20
"""
    int: size in bytes of all script hashes
"""
ADDRESS_SIZE = PREFIX_SIZE + SH_SIZE
"""
    int: size in byte of all P2SH addresses
"""


# Classes
class P2SH(AddressType):
    """
    Pay to script hash address. Allows to serialize, deserialize, encode
    and decode P2SH addresses so the reedem script hash can be easily set and
    got (its hash) to generate / decode easily P2SH addresses

    Internal _value field is used as it contains the hash of the reedem script
    itself
    """

    def __init__(self):
        """ Same as Address constructor, but setting correct type """
        super().__init__(Types.p2sh)

    def deserialize(self, address):
        """
        Deserializes the given address as an array of bytes, guessing its
        prefix and saving its info, checking that the prefix type is P2SH and
        after that, setting the script hash value

        Args:
            address (bytes): bytes object containing an address to deserialize

        Returns:
            self: the object with the updated values
        """
        # Check size
        if len(address) != ADDRESS_SIZE:
            raise ValueError("""P2SH Address %s size in bytes is not valid.
        All P2SH addresses have %d bytes""" % (address.hex(), ADDRESS_SIZE))
        # Basic deserialization
        super().deserialize(address)
        return self

    @property
    def value(self):
        """ Returns the address data (script hash) """
        return self._value

    @value.setter
    def value(self, value):
        """ Sets the address value (script hash) """
        self.script_hash = value

    @property
    def script_hash(self):
        """ Extracts the script hash from the address, it's the same as the
        address value """
        return self._value

    @script_hash.setter
    def script_hash(self, script_hash):
        """ Sets the reedem script hash, updating address value """
        # Check size
        if len(script_hash) != SH_SIZE:
            raise ValueError("""Unable to set a reedem script hash with length
            %d bytes. Script hash has to be %d bytes""" % (len(script_hash),
                                                           SH_SIZE))
        # Update values
        self._value = script_hash
