"""
Models a P2PKH scriptSig script, autobuilding the necessary opcodes to create
the P2PKH
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
    __slots__ = ["_input", "_signature", "_public_key"]

    def __init__(self, tx_input=None):
        """
        Initializes a P2PKH scriptsig given its input it belongs to

        Args:
            tx_input (TxInput): input the script belongs to
        """
        super().__init__(tx_input)
        self._signature = None
        self._public_key = None

    def serialize(self):
        """
        Checks that it has been signed before serializing
        """
        assert self._signature is not None and self._public_key is not None, \
            "The P2PKH can't be serialized as it has not been signed"
        return super().serialize()

    def _build(self):
        """
        Appends data to the script given the signature and public key
        """
        self._data = [
            ScriptData(self._signature), ScriptData(self._public_key)]

    def sign(self, key, script=None, hashtype=DEFAULT_HASHTYPE):
        """
        Due to there's needed a signature, this is the class where the sign
        method should be. Already not decided how to implement that.

        Args:
            key (bytes): private key to create the signature and public key
            script (ScriptPubKey): pubkey script to place in the input in order
            to generate the signature
            hashtype (HashType.item): hashtype to use to create signature
        """
        assert isinstance(self._input.tx, SignableTx)
        self._public_key = private_to_public(key)
        if script is None:
            # Create a P2PKH pubkey script from key to sign
            script = address.P2PKH(public_key=self._public_key).script
        self._signature = self._input.tx.sign(
            key, self._input, script, hashtype)

        self._build()

    @property
    def is_signed(self):
        """ Returns True if has been signed, false otherwise """
        return self._signature is not None and self._public_key is not None

    @property
    def signature(self):
        """ Returns the signature stored in the P2PKH script or None if has
        not been signed yet"""
        return self._signature

    @property
    def public_key(self):
        """ Returns the public key stored in the P2PKH script or None if has
        not been signed yet"""
        return self._public_key

    def __len__(self):
        """ Returns the script length """
        return 0 if not self.is_signed else super().__len__()

    def __str__(self):
        """
        Returns the scriptSig in a printable way
        """
        return "<%s:%s(%s)>" % (
            "|Not signed yet|" if not self.is_signed else
            "|Signature & Public key|",
            self.__class__.__name__, " ".join(map(str, self._data)))
        return
