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
from bitcoin import base58
from ..field.model import Field
from ..interfaces import Base58Encodable
from ..nets import Network
from .types import Types
from . import prefix
from . import helper


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
            addr_net, addr_type, addr_prefix = helper.guess_prefix(addr_prefix)
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

    def encode(self):
        """
        Returns the address as a base-58 string of the array of bytes (the
        serialized address)
        """
        return base58.encode(self.serialize())

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
        addr_net, addr_type, addr_prefix = helper.guess_prefix(address)
        value = address[len(addr_prefix):]
        return cls(value)

    @classmethod
    def decode(cls, address):
        """
        Given a base-58 encoded address, decodes it and deserializes it saving
        the information of the address passed into the object. Raises an
        exception if the address given can't be decoded

        Args:
            address (str): base-58 encoded address string

        Returns:
            Address: the address itself, filled with the values

        Raises:
            ValueError: if address can't be decoded
        """
        return cls.deserialize(base58.decode(address))

    @property
    def network(self):
        """ Returns the network the address belongs to """
        return self._net

    @network.setter
    def network(self, network):
        """ Sets a new network, changing the prefix according to it """
        self._prefix = prefix.get(network, self._type.name)
        self._net = network

    @property
    def type(self):
        """ Returns the type of the address """
        return self._type

    @property
    def prefix(self):
        """ Returns the bytes prefix of the address """
        return self._prefix

    @prefix.setter
    def prefix(self, prefix):
        """
        Sets the address prefix. Checks for the network and type of the prefix
        and updates them too. If the prefix is unknown, Exception is raised.

        Prefix can't be changed if it means the address type will be changed
        and is a known type

        Args:
            prefix (bytes): prefix to set

        Raises:
            ValueError: if the type changes or the prefix is invalid
        """
        # Assert type
        assert isinstance(prefix, bytes), """Prefix must be a bytes object"""

        # Guess new network and type
        guess = prefix.guess(prefix)

        # Invalid prefix
        if guess is None:
            raise ValueError("""Invalid prefix %s tried to set""" %
                             prefix.hex())

        addr_net, addr_type = guess
        # Check type hasn't changed
        if addr_type != self._type:
            raise ValueError("""Prefix must be of the same address type""")

        # Set
        self._prefix = prefix
        self._net = addr_net
        self._type = addr_type

    @property
    def value(self):
        """ Returns the address data """
        return self._value

    @value.setter
    def value(self, value):
        """ Sets the address data """
        self._value = value
