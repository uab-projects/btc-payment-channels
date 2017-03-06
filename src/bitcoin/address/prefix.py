"""
Defines the prefixes available for addresses in the Bitcoin cryptocurrency
according if they belong to the testnet or to the mainnet

Prefixes extracted from:
    https://en.bitcoin.it/wiki/List_of_address_prefixes
"""
from enum import Enum, unique
from ..nets import Network


@unique
class Types(Enum):
    """
    Defines the types a Bitcoin address can be
    """
    unknown = -1
    p2pkh = 1
    p2sh = 2
    wif_pkey = 3
    bip32_pubkey = 4
    bip32_pkey = 5


class Prefixes(object):
    """
    Defines what prefixes every network must define to use for their addresses

    All prefixes must be bytes objects

    Attributes:
        p2pkh (bytes): prefix for pubkey hash addresses
        p2sh (bytes): prefix for pay-to-script hash addresses
        wif_pkey (bytes): prefix for WIF private key / pubkey
        bip32_pubkey (bytes): prefix for BIP32 public keys
        bip32_pkey (bytes): prefix for BIP32 private keys
    """
    __slots__ = ["_p2pkh", "_p2sh", "_wif_pkey", "_bip32_pubkey",
                 "_bip32_pkey"]

    def __init__(self):
        """
        Initializes all prefixes with empty lists
        """
        self._p2pkh = None
        self._p2sh = None
        self._wif_pkey = None
        self._bip32_pubkey = None
        self._bip32_pkey = None

    @classmethod
    def _check_type(cls, address, prefix):
        """
        Given an address and a list of prefixes, check if the address starts
        with the prefix and returns true if it's the case or false
        if not

        Args:
            address (bytes): address as a bytes object
            prefix (byte): prefix to check

        Returns:
            bool: True if the address belongs to one of the prefixes
        """
        return prefix is not None and address.startswith(prefix)

    def get_type(self, address):
        """
        Given an address, looks in all prefixes and returns the type of address

        Args:
            address (bytes): address as a bytes object

        Returns:
            Types.
        """
        # Check all types
        if self._check_type(address, self._p2pkh):
            return Types.p2pkh
        elif self._check_type(address, self._p2sh):
            return Types.p2sh
        elif self._check_type(address, self._wif_pkey):
            return Types.wif_pkey
        elif self._check_type(address, self._bip32_pubkey):
            return Types.bip32_pubkey
        elif self._check_type(address, self._bip32_pkey):
            return Types.bip32_pkey
        else:
            return Types.unknown

    @property
    def p2pkh(self):
        """ Returns the p2pkh attribute """
        return self._p2pkh

    @property
    def p2sh(self):
        """ Returns the p2sh attribute """
        return self._p2sh

    @property
    def wif_pkey_u(self):
        """ Returns the wif_pkey attribute """
        return self._wif_pkey

    @property
    def bip32_pubkey(self):
        """ Returns the bip32_pubkey attribute """
        return self._bip32_pubkey

    @property
    def bip32_pkey(self):
        """ Returns the bip32_pkey attribute """
        return self._bip32_pkey

    @property
    def all_prefixes(self):
        """ Returns a list with all prefixes """
        return self._p2pkh + self._p2sh + self._wif_pkey + \
            self._bip32_pubkey + self._bip32_pkey


class MainNetPrefixes(Prefixes):
    """
    Defines the mainNet prefixes for Bitcoin addresses
    """

    def __init__(self):
        """
        Initializes the class with the values of the mainNet prefixes
        """
        super().__init__()
        self._p2pkh = b'\x00'
        self._p2sh = b'\x05'
        self._wif_pkey = b'\x80'
        self._bip32_pubkey = b'\x04\x88\xB2\x1E'
        self._bip32_pkey = b'\x04\x88\xAD\xE4'


class TestNetPrefixes(Prefixes):
    """
    Defines the testNet prefixes for Bitcoin addresses
    """

    def __init__(self):
        """
        Initializes the class with the values of the testNet prefixes
        """
        super().__init__()
        self._p2pkh = b'\x6F'
        self._p2sh = b'\xC4'
        self._wif_pkey = b'\xEF'
        self._bip32_pubkey = b'\x04\x35\x87\xCF'
        self._bip32_pkey = b'\x04\x35\x83\x94'


def create_networks_prefixes():
    """
    Generates a Python dictionary containing for each Network defined in
    the nets module with available prefixes a prefixes object with the prefixes
    for addresses in that network

    Returns:
        dict: dictionary with networks as keys and prefixes objects as values
    """
    return {
        Network.mainnet: MainNetPrefixes(),
        Network.testnet: TestNetPrefixes()
    }
