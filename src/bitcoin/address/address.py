"""
Models a Bitcoin address and provides methods to check its type and generate
them given the type and value

Information about addresses can be found here:
https://en.bitcoin.it/wiki/Address
https://en.bitcoin.it/wiki/List_of_address_prefixes
"""
# Libraries
from bitcoin import base58
from hashlib import sha256
from ..field.model import Field
from ..nets import Network
from . import prefix


class Address(Field):
    """
    The address class allows to generate and verify addresses in an easy way

    Attributes:
        _net (Network): network the address belongs to
        _type (prefix.Types): type of the address
        _value (bytes): address as a byte object
        _prefix (bytes): the address prefix
    """
    __slots__ = ["_net", "_type", "_value"]

    def __init__(self, address, address_type=prefix.Types.unknown,
                 net=Network.unknown):
        """
        Initializes an address, given the address value as a bytes object and
        optionally the network of the address. If no network or type are
        specified, they will be guessed.

        Args:
            address (bytes): address as a bytes object (without base58 encode)
            net (Network): network the address belongs to
        """
        # Create groups
        prefix_groups = prefix.create_networks_prefixes()
        # Guess network and type
        if net == Network.unknown or address_type == prefix.Types.unknown:
            # Guess missing values
            if net != Network.unknown:
                # Guess type
                address_type = prefix_groups[net].get_type(address)
            else:
                # Guess both values
                for network, prefixes in prefix_groups.items():
                    address_type = prefixes.get_type(address)
                    if address_type != prefix.Types.unknown:
                        net = network
                        break
            # Check if guessed
            if address_type == prefix.Types.unknown:
                raise ValueError("""The address (%s) is not related to any
                defined network or prefix for any network""" % (address.hex()))
        # Set values
        self._net = net
        self._type = address_type
        self._value = address
        self._prefix = getattr(prefix_groups[self._net], self._type.name)

    @classmethod
    def from_address_string(cls, address_str,
                            address_type=prefix.Types.unknown,
                            net=Network.unknown):
        """
        Initializes an address object, but given the base58 encoded string
        instead of the bytes object. If no network or type are
        specified, they will be guessed.

        Args:
            value (str): address as a string (base58 encoded)
            net (Network): network the address belongs to

        Returns:
            Address: address object instance
        """
        return cls(base58.decode(address_str), address_type, net)

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
    def data(self):
        """ Returns the data stored in the address, that will depend on the
        type """
        return self._value[len(self._prefix):]


class P2PKH(Address):
    """
    Address of type P2PKH. Provides method to check the checksum, and extract
    the public key hash from the address
    """
    SIZE = 25
    """
        int: size in bytes of all P2PKH addresses
    """
    CHECKSUM_SIZE = 4
    """
        int: size in bytes for the address suffix checksum
    """

    def __init__(self, address, address_type=prefix.Types.unknown,
                 net=Network.unknown):
        """ Same as Address constructor, but checking type is correct """
        super().__init__(address, address_type, net)
        # Check type and validate
        assert self._type == prefix.Types.p2pkh, "P2PKH address type invalid"
        self._validate()

    def _validate(self):
        """
        Checks the address is valid by checking its size and checksum

        Raises:
            ValueError: if the address contains an error
        """
        # Check length
        if len(self._value) != self.SIZE:
            raise ValueError("""P2PKH Address %s size in bytes is different than
            %d""" % (self._value.hex(), self.SIZE))
        # Check checksum
        guess_checksum = sha256(sha256(
            self._prefix + self.data).digest()).digest()[:self.CHECKSUM_SIZE]
        if guess_checksum != self.checksum:
            raise ValueError("""P2PKH Address has invalid checksum. Calculated
                checksum is %s, given is %s""" % (guess_checksum.hex(),
                                                  self.checksum.hex()))

    @property
    def data(self):
        """ Extracts the public key hash from the address """
        return super().data[:-self.CHECKSUM_SIZE]

    @property
    def checksum(self):
        """ Returns the address checksum """
        return self._value[-self.CHECKSUM_SIZE:]


# Testing
if __name__ == "__main__":
    # Test all addresses types and check if guesses are OK
    cases = [
        ("1BoatSLRHtKNngkdXEeobR76b53LETtpyT",
         Network.mainnet, prefix.Types.p2pkh),
        ("mgcjJSFdTZSajvW2RqYAzHjf9RgmL3BQZ4",
         Network.testnet, prefix.Types.p2pkh),
        ("2NByaYwku2jFiaUhgnJxo3s695G5v6dzNBf",
         Network.testnet, prefix.Types.p2sh)
    ]
    print("Testing Addresses module")
    # Loop and test
    for case in cases:
        # Initialize test case
        address_str, net, address_type = case
        print("  Testing Address %s" % (address_str))
        print("    -> Net: %s, Type: %s" % (net.name, address_type.name))
        # Test guessing everything
        address_obj = Address.from_address_string(address_str)
        print("    -> Guess net and type: ", end='')
        if address_obj.type == address_type and address_obj.network == net:
            print("pass")
        else:
            raise ValueError("failed. Network or type invalid: %s / %s" %
                             (address_obj.net, address_obj.type))
        # Test guessing just network
        address_obj = Address.from_address_string(address_str, address_type)
        print("    -> Guess just network: ", end='')
        if address_obj.type == address_type and address_obj.network == net:
            print("pass")
        else:
            raise ValueError("failed. Network or type invalid: %s / %s" %
                             (address_obj.net, address_obj.type))
        # Test guessing just type
        address_obj = Address.from_address_string(address_str, net=net)
        print("    -> Guess just type: ", end='')
        if address_obj.type == address_type and address_obj.network == net:
            print("pass")
        else:
            raise ValueError("failed. Network or type invalid: %s / %s" %
                             (address_obj.net, address_obj.type))
        # Guessed prefix
        print("    -> Guessed byte-prefix: %s" % address_obj.prefix.hex())
        # Specific class test
        if address_type == prefix.Types.p2pkh:
            print("    -> Validating P2PKH address: ", end='')
            address_obj = P2PKH.from_address_string(address_str)
            print("pass")
