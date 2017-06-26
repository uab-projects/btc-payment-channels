"""
Provides a signable transaction, with methods to create a pseudo-transaction to
sign
"""
# Libraries
# # Built-in
from enum import Enum
import copy

# # App
from .model import BasicTx
from .. import script
from ..field.general import U4BLEInt
from ..crypto import ecdsa
from ..crypto.hash import double_sha256


# Enums
class HashTypes(Enum):
    """
    Hashtypes available to create signable transactions as specified in:
    https://en.bitcoin.it/wiki/OP_CHECKSIG
    """
    all = b'\x01'
    none = b'\x02'
    single = b'\x03'
    anyonecanpay = b'\x80'


# Constants
DEFAULT_HASHTYPE = HashTypes.all
"""
    HashType.item: default hashtype to use if not specified
"""


# Class
class SignableTx(BasicTx):
    """
    Defines a transaction that can be signed, providing methods to create a
    pseudo-transaction that will be signed using ECDSA algorithms
    """
    def signable_tx(self, input_num, script_pubkey,
                    hashtype=DEFAULT_HASHTYPE):
        """
        Given an input that requires to be signed, the pubkey script that the
        input refers to, and the hashtype to use to create the signable tx,
        creates a copy of the present transaction and returns a signable copy
        with all inputs and outputs treated according to the hashtype passed
        and with the given input script changed to the pubkey script given

        Source:
        https://en.bitcoin.it/wiki/OP_CHECKSIG
        https://github.com/vbuterin/pybitcointools/blob/master/bitcoin/transaction.py

        Args:
            input_num (int): number of input to change it's script
            you can also provide the input object and we'll search for its num
            script_pubkey (script.pubkey): script to set in the input
            hashtype (HashType item): hashtype to use. Default will be used if
            empty
        """
        # Check types
        assert len(self.inputs), """There aren't any inputs to sign"""
        from ..io.input import TxInput
        if isinstance(input_num, TxInput):
            try:
                input_num = self.inputs.index(input_num)
            except ValueError:
                raise ValueError("The input passed has not been found")
        assert isinstance(input_num, int), """Input must be a number"""
        assert input_num >= 0 and input_num < len(self.inputs), """Input number
        does not match any input (%d is not 0 <= num < %d)""" % (
            input_num, len(self.inputs))
        # assert isinstance(script_pubkey, script.pubkey.ScriptPubKey), \
        #    "The script pubkey must be a ScriptPubKey object"
        assert isinstance(hashtype, HashTypes), """The hashtype must be a """
        """HashType enum item"""
        # Copy transaction
        signable_tx = copy.deepcopy(self)
        # Empty all scripts
        for tx_in in signable_tx.inputs:
            tx_in.script.input = tx_in
            tx_in.script = script.ScriptSig()
        # Assign the pubkey script to the input script
        signable_tx.inputs[input_num].script = script_pubkey
        # Apply hashtype
        if hashtype == HashTypes.none:
            # No outputs are signed
            signable_tx.outputs = []
        elif hashtype == HashTypes.single:
            # Just the matching output is signed
            # Same number of outputs as inputs
            signable_tx.outputs = signable_tx.outputs[:len(signable_tx.inputs)]
            # Empty outputs except the last
            for out in signable_tx.outputs[:len(signable_tx.inputs)-1]:
                out.value = 2**64-1
                out.script = script.pubkey.ScriptPubKey()
        elif hashtype == HashTypes.anyonecanpay:
            signable_tx.inputs = [signable_tx.inputs[input_num]]
        return signable_tx

    def signable_hash(self, hashtype=DEFAULT_HASHTYPE):
        """
        Returns the hash needed to perform signatures given the hashtype that
        will be used

        Args:
            hashtype (HashType item): hashtype to use. Default will be used if
            empty
        """
        hashtype_field = U4BLEInt(int.from_bytes(hashtype.value, "big"))
        signable_bytes = self.serialize() + hashtype_field.serialize()
        return double_sha256(signable_bytes)

    def sign(self, key, input_num, script_pubkey, hashtype=DEFAULT_HASHTYPE):
        """
        Signs the current transaction for the given input number, by generating
        a signable transaction using the _signable_tx method with the same
        arguments and then performing the signature using the private key
        given

        Args:
            key (bytes): private key to sign as a bytes object
            input_num (int): number of input to change it's script
            script_pubkey (script.pubkey): script to set in the input
            hashtype (HashType item): hashtype to use. Default will be used if
            empty

        Returns:
            bytes: bytes object containing the signature
        """
        # Create signable transaction for the input
        signable_tx = self.signable_tx(input_num, script_pubkey, hashtype)
        return ecdsa.der_sign(signable_tx.signable_hash(), key) + \
            hashtype.value
