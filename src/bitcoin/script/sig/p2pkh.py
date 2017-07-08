"""
Models a P2PKH scriptSig script, autobuilding the necessary opcodes to create
the P2PKH script containing the signature and public key
"""
# Libraries
from .model import ScriptSig
from ... import address
from ...field.script import ScriptData
from ...crypto.ecdsa import private_to_public
from ...tx import DEFAULT_HASHTYPE, SignableTx


class P2PKH(ScriptSig):
    """
    Basic pay-to-public-key-hash scriptsig.

    Sources:
    https://en.bitcoin.it/wiki/Transaction#Pay-to-PubkeyHash

    Args:
        _signature (bytes): ECDSA signature for the input and transaction
        _public_key (bytes): Public key whose private key generated the
        signature
    """
    __slots__ = ["_signature", "_public_key"]

    def __init__(self, tx_input=None):
        """
        Initializes a P2PKH scriptsig given its input it belongs to

        Args:
            tx_input (TxInput): input the script belongs to
        """
        super().__init__(tx_input)
        self._signature = None
        self._public_key = None

    def _build(self):
        """
        Creates the scriptSig containing the signature and public key
        """
        # Check it has been signed
        assert self._signature is not None and self._public_key is not None, \
            "The P2PKH can't be serialized as it has not been signed"
        self._data = [
            ScriptData(self._signature), ScriptData(self._public_key)]

    def sign(self, key, script=None, hashtype=DEFAULT_HASHTYPE):
        """
        Signs the transaction the script belongs to with the key given,
        changing the input to sign script (this related input) with the passed
        script, and with the hashtype given

        Args:
            key (bytes): private key to create the signature and public key
            script (ScriptPubKey): pubkey script to place in the input in order
            to generate the signature. If not specified, will be a P2PKH one
            automatically generated from the public key of the key given
            hashtype (HashType.item): hashtype to use to create signature
        """
        # Assert can be signed
        assert self.input is not None and self.input.tx is not None, \
            "To sign the P2PKH scriptSig, there must be an input related " + \
            "to the scriptSig that is related to a transaction"
        assert isinstance(self.input.tx, SignableTx), "To sign the P2PKH " + \
            "scriptSig, the related transaction must be a SignableTx"
        # Get public key
        self._public_key = private_to_public(key)
        # Create script if necessary
        if script is None:
            # Create a P2PKH pubkey script from key to sign
            script = address.P2PKH(public_key=self._public_key).script
        # Sign and add
        self._signature = self.input.tx.sign(
            key, self.input, script, hashtype)

    @property
    def is_signed(self):
        """
        Returns True if has been signed, false otherwise
        """
        return self._signature is not None and self._public_key is not None

    @property
    def signature(self):
        """
        Returns the signature stored in the P2PKH script or None if has
        not been signed yet
        """
        return self._signature

    @property
    def public_key(self):
        """
        Returns the public key stored in the P2PKH script or None if has
        not been signed yet
        """
        return self._public_key

    def __len__(self):
        """ Returns the script length """
        return 0 if not self.is_signed else super().__len__()

    def __str__(self, space):
        """
        Returns the scriptSig in a printable way
        """
        return "<%s:%s(%s)>" % (
            "|Not signed yet|" if not self.is_signed else
            "|Signature & Public key|",
            self.__class__.__name__, " ".join(map(str, self._data)))
        return
