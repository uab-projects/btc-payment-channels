"""
Defines a class to model a P2SH address, this means, adding extra methods to
set the reedem script and generate the address automatically

Information extracted from:
http://www.soroushjp.com/2014/12/20/bitcoin-multisig-the-hard-way-understanding-raw-multisignature-bitcoin-transactions/
"""
# Libraries
# # App
from .model import Address
from .types import Types
from ..script.redeem import RedeemScript
from ..script import pubkey
from ..nets import DEFAULT_NETWORK
from ..crypto.hash import checksum

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
CHECKSUM_SIZE = 4
"""
    int: size in bytes for the address suffix checksum
"""


# Classes
class P2SH(Address):
    """
    Pay to script hash address. Allows to serialize, deserialize, encode
    and decode P2SH addresses so the reedem script hash can be easily set and
    got (its hash) to generate / decode easily P2SH addresses

    Internal _value field is contains the hash of the reedem script itself
    """
    def __init__(self, redeem_script=None, addr_net=DEFAULT_NETWORK,
                 redeem_script_hash=None):
        """
        Initializes a P2SH address with the network it belongs to and the
        redeem script hash or the redeem script, so the redeem script hash
        is automatically set.

        You can set either the redeem script object so the hash is performed
        and then set in the address value or directly the hash as a bytes
        object. If both are passed, just the bytes object is taken.

        Args:
            addr_net (Network): network the address belongs to
            redeem_script (RedeemScript): redeem script to build the key on
            redeem_script_hash (bytes): redeem script hash to set as value
        """
        # Type assertions
        assert isinstance(redeem_script, RedeemScript) \
            or redeem_script is None, """Redeem script must be a RedeemScript
            object"""
        assert isinstance(redeem_script_hash, bytes) \
            or redeem_script_hash is None, """Redeem script hash must be a bytes
            object"""
        assert redeem_script is not None or redeem_script_hash is not None, \
            """You must specify either a redeem script or a redeem script hash
            to create a P2SH address"""

        # Initialize super
        super().__init__(Types.p2sh, addr_net)

        # Set value
        if redeem_script_hash is not None:
            assert len(redeem_script_hash) == SH_SIZE, """Unable to set a
            reedem script hash with length %d bytes. Script hash has to be %d
            bytes""" % (len(redeem_script_hash), SH_SIZE)
            self._value = redeem_script_hash
        else:
            self._value = redeem_script.hash
        # Add checksum
        self._value += checksum(self._prefix + self._value)

    @classmethod
    def deserialize(cls, address):
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
        assert len(address) == ADDRESS_SIZE, """P2SH Address %s size in bytes
        is not valid. All P2SH addresses have %d bytes""" % (
            address.hex(), ADDRESS_SIZE)
        # Basic deserialization
        addr_obj = Address.deserialize(address)
        # Check type
        assert addr_obj.type == Types.p2sh, """The deserialized address is not
        a P2SH address"""
        # Return object
        return cls(addr_net=addr_obj.network,
                   redeem_script_hash=addr_obj.value)

    @property
    def checksum(self):
        """ Returns the p2sh address checksum """
        return self._value[-CHECKSUM_SIZE:]

    @property
    def script_hash(self):
        """ Extracts the script hash from the address, it's the same as the
        address value """
        return self._value[:-CHECKSUM_SIZE]

    @property
    def script(self):
        """ Returns a P2SH scriptpubkey that pays to this P2SH address """
        return pubkey.P2SH(self)
