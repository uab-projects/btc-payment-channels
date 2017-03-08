"""
Models a Bitcoin address and provides methods to check its type and generate
them given the type and value

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

    def __init__(self):
        """
        Initializes an empty address, without any predefined network, type
        or address
        """
        self._value = bytes()
        self._net = Network.unknown
        self._type = prefix.Types.unknown
        self._prefix = bytes()

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

    def _guess_prefix(self, address):
        """
        Given an address, tries to gets its prefix and therefore the type and
        network of it. If it succeeds, saves the values to the class, if not,
        raises an Exception. Also checks that if the address has a valid type,
        (type is not unknown) the prefix is not changing it, as it could led to
        errors.

        Args:
            address (bytes): address to guess prefix from

        Raises:
            ValueError: if prefix can't be guessed
            ValueError: if type has to be changed due to the new prefix
        """
        # Guess type and network
        guess_info = prefix.guess(address)

        # Check if guessed
        if guess_info is None:
            raise ValueError("""The address (%s) is not related to any
            defined network or prefix for any network""" % (address.hex()))
        else:
            guess_network, guess_type = guess_info

        # Check type
        if self._type != Types.unknown and self._type != guess_type:
            raise ValueError("""The address (%s) type (%s) is not valid for this
            object. This object requires an address of type %s""" (
                address.hex(), guess_type.name, self._type.name))

        # Save values
        self._net = guess_network
        self._type = guess_type
        self._prefix = prefix.get(guess_network, guess_type.name)

    def deserialize(self, address):
        """
        Given an address an array of bytes, try to guess information from the
        address (type of address, network and prefix) by looking into the
        defined prefixes. After that, saves the address value and guessed
        information into the object.

        If the current address object has a type, checks that the
        deserialization doesn't change the type, to prevent mistakes.

        Args:
            address (bytes): bytes object containing an address to deserialize

        Returns:
            self: the object with the updated values
        """
        self._guess_prefix(address)
        self._value = address[len(self._prefix):]
        return self

    def decode(self, address):
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
        self.deserialize(base58.decode(address))
        return self

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

    @prefix.setter
    def prefix(self, prefix):
        """
        Sets the address prefix. Checks for the network and type of the prefix
        and updates them too. If the prefix is unknown, Exception is raised.

        Prefix can't be changed if it means the address type will be changed
        and is a known type

        Args:
            prefix (bytes): prefix to set
        """
        self._guess_prefix(prefix)

    @property
    def value(self):
        """ Returns the address data """
        return self._value

    @value.setter
    def value(self, value):
        """ Sets the address value """
        self._value = value


class AddressType(Address):
    """
    Fixed-type address, but whose network may change. This means that when
    deserializing, the type is checked to ensure it doesn't change and that
    when the network is changed, the prefix is calculated automatically
    """
    def __init__(self, address_type):
        """
        Initializes and empty address with its type

        Args:
            address_type (Types): type of the address
        """
        super().__init__()
        self._type = address_type

    @property
    def network(self):
        """ Returns the network the address belongs to """
        return self._net

    @network.setter
    def network(self, network):
        """ Sets a new network, changing the prefix according to it """
        self._prefix = prefix.get(network, self._type.name)
        self._net = network
