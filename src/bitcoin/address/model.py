"""
Models a Bitcoin address and provides methods to check its type and generate
them given the type and value

A Bitcoin address is not just the public key hash to pay in a P2PKH script, it
also can contain a private key, a public key, or a script hash for their use
in P2SH pubkey scripts

Information about addresses can be found here:
https://en.bitcoin.it/wiki/Address
https://en.bitcoin.it/wiki/List_of_address_prefixes
"""
# Libraries
# # App
from ..field.model import Field
from ..interfaces import Base58Encodable
from ..nets import Network
from .types import Types
from . import prefix


class Address(Field, Base58Encodable):
    """
    The address class allows to deserialize and serialize addresses from and
    to an array of bytes, obtaining basic data about them like the address
    prefix, and therefore, the address type and network

    Value property saved is the data the address contains, that depending on
    the address type has different meanings. Value is the address without the
    prefix.

    Attributes:
        _net (Network): network the address belongs to
        _type (prefix.Types): type of the address
        _prefix (bytes): the address prefix
        _value (bytes): address data (address without prefix) as a bytes object
    """
    __slots__ = ["_net", "_type", "_prefix"]

    def __init__(self, addr_type=prefix.Types.unknown,
                 addr_net=Network.unknown, addr_prefix=None, value=None):
        """
        Initializes an empty address given the type of address and network they
        belong to or the prefix of the address

        Either a valid address type and network must be provided or just the
        prefix so the network and type are guessed automatically. If not, an
        exception will be raised

        If given all arguments, just network and type will be used

        Args:
            addr_type (address.Types): type of the address
            addr_net (bitcoin.Nets): network of the address
            addr_prefix (bytes): address prefix as bytes
            value (bytes): value of the address as a bytes object

        Raises:
            ValuError: if no type / network combination or prefix has been
                       specified
        """
        # Assert types
        assert isinstance(addr_type, Types), """Type must be an address.Types
        enum value"""
        assert isinstance(addr_net, Network), """Network must be a
        bitcoin.Network enum value"""
        assert isinstance(addr_prefix, bytes) or addr_prefix is None, """Prefix
        must be a bytes object"""
        assert isinstance(value, bytes) or value is None, """Value must be
        either None or a bytes object"""
        # Check pairs
        if addr_type != Types.unknown and addr_net != Network.unknown:
            # Got a type / network pair
            addr_prefix = prefix.get(addr_net, addr_type.name)
        elif addr_prefix is not None:
            # Got a prefix
            guess_info = prefix.guess(addr_prefix)
            assert guess_info is not None, "The prefix (%s) is not valid" % (
                addr_prefix.hex())
            addr_net, addr_type = guess_info
        else:
            raise ValueError("""You must specify either a valid network and
            type of address combination or a prefix as a bytes object to build
            an address""")
        # Assign values
        self._value = value if value is not None else bytes()
        self._net = addr_net
        self._type = addr_type
        self._prefix = addr_prefix

    def serialize(self):
        """
        Returns the address as an array of bytes by composing the value and
        the prefix
        """
        return self.prefix + self.value

    @classmethod
    def deserialize(cls, address):
        """
        Given an address an array of bytes, try to guess information from the
        address (type of address, network and prefix) by looking into the
        defined prefixes. After that, saves the address value and guessed
        information into a new object.

        Args:
            address (bytes): bytes object containing an address to deserialize

        Returns:
            self: the object with the updated values
        """
        guess_info = prefix.guess(address)
        # Validate given information
        assert guess_info is not None, """The address (%s) is not valid, no
        valid prefix has been found""" % (address.hex())
        addr_net, addr_type = guess_info
        # Get prefix
        addr_prefix = prefix.get(addr_net, addr_type.name)
        # Get value
        value = address[len(addr_prefix):]
        return cls(addr_prefix=addr_prefix, value=value)

    @property
    def network(self):
        """ Returns the network the address belongs to """
        return self._net

    @property
    def type(self):
        """ Returns the type of the address """
        return self._type

    @property
    def prefix(self):
        """ Returns the bytes prefix of the address """
        return self._prefix

    @property
    def value(self):
        """ Returns the address data """
        return self._value

    def __str__(self):
        """ Returns the field as a printable string """
        return "<%s:%s(net=%s)>" % (
            self.encode(), self.__class__.__name__, self._net)
