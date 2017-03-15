"""
Tests the address module with some addresses
"""
# Libraries
from bitcoin import base58
from ..nets import Network
from .prefix import Types
from .model import Address
from .p2pkh import P2PKH
from .wif import WIF


# Constants
CASES = [
    ("1BoatSLRHtKNngkdXEeobR76b53LETtpyT",
     Network.mainnet, Types.p2pkh),
    ("mgcjJSFdTZSajvW2RqYAzHjf9RgmL3BQZ4",
     Network.testnet, Types.p2pkh),
    ("2NByaYwku2jFiaUhgnJxo3s695G5v6dzNBf",
     Network.testnet, Types.p2sh),
    ("5JePNVcofSQgVoLtkLVwDsRsoUgyBKFJa8q17XRUsikDnjDH1Tt",
     Network.mainnet, Types.wif)
]
"""
    dict: test cases, containing a real address, and the supposed network and
    type
"""

# Testing
if __name__ == "__main__":
    # Test all addresses types and check if guesses are OK
    print("Testing Addresses module")
    # Loop and test
    for case in CASES:
        # Initialize test case
        address_str, net, address_type = case
        print("  Testing Address %s" % (address_str))
        print("    -> Net: %s, Type: %s" % (net.name, address_type.name))
        # Some variables
        address_bytes = base58.decode(address_str)
        # Test decoding and deserializing
        address_obj = Address().decode(address_str)
        print("    -> Decode test: ", end="")
        if address_obj.type == address_type and address_obj.network == net:
            print("pass")
        else:
            raise ValueError("failed. Network or type invalid: %s / %s" %
                             (address_obj.net, address_obj.type))
        print("    -> Guessed byte-prefix: %s" % address_obj.prefix.hex())
        # Test encoding and serializing
        address_prefix = address_obj.prefix
        address_value = address_bytes[len(address_prefix):]
        print("    -> Encode test: ", end="")
        address_obj = Address()
        address_obj.prefix = address_prefix
        address_obj.value = address_value
        address_encoded = address_obj.encode()
        if address_encoded == address_str:
            print("pass")
        else:
            raise ValueError("failed. Unable to re-encode address %s" %
                             (address_str))
        # Specific class test
        if address_type == Types.p2pkh:
            print("    -> Specific P2PKH test")
            print("        -> Decoding P2PKH address: ", end='')
            address_obj = P2PKH().decode(address_str)
            print("pass")
            address_pkh = address_obj.pkh
            address_checksum = address_obj.checksum
            print("        -> Guessed pkh: %s (%d-byte)" % (address_pkh.hex(),
                                                            len(address_pkh)))
            print("        -> Guessed checksum: %s (%d-byte)" % (
                address_checksum.hex(), len(address_checksum)))
            print("        -> Encoding P2PKH address: ")
            address_obj = P2PKH()
            address_obj.network = net
            address_obj.pkh = address_pkh
            print("        -> Got prefix: %s" % address_obj.prefix.hex())
            print("        -> Got pkh: %s (%d-byte)" % (address_obj.pkh.hex(),
                                                        len(address_obj.pkh)))
            print("        -> Got checksum: %s (%d-byte)" % (
                address_obj.checksum.hex(), len(address_obj.checksum)))
            if address_obj.encode() == address_str:
                print("        -> Test pass")
            else:
                raise ValueError("""Unable to encode address %s from its network
                and public key hash""" % (address_str))
        elif address_type == Types.wif:
            print("    -> Specific WIF test")
            print("        -> Decoding WIF address: ", end='')
            address_obj = WIF().decode(address_str)
            print("pass")
            address_pkey = address_obj.private_key
            address_checksum = address_obj.checksum
            print("        -> Guessed private key: %s (%d-byte)" % (
                address_pkey.hex(), len(address_pkey)))
            print("        -> Guessed checksum: %s (%d-byte)" % (
                address_checksum.hex(), len(address_checksum)))
            print("        -> Encoding WIF address: ")
            address_obj = WIF()
            address_obj.network = net
            address_obj.private_key = address_pkey
            print("        -> Got prefix: %s" % address_obj.prefix.hex())
            print("        -> Got private key: %s (%d-byte)" % (
                address_obj.private_key.hex(), len(address_obj.private_key)))
            print("        -> Got checksum: %s (%d-byte)" % (
                address_obj.checksum.hex(), len(address_obj.checksum)))
            if address_obj.encode() == address_str:
                print("        -> Test pass")
            else:
                raise ValueError("""Unable to encode address %s from its network
                and public key hash""" % (address_str))
