"""
More information could be found in:
https://bitcoin.org/en/developer-guide#standard-transactions
"""
from .general import Script
from ..field.script import StackDataField
from .hashcodes import Types
from pybitcointools import deserialize, signature_form, privkey_to_pubkey,\
                    pubkey_to_address, mk_pubkey_script, ecdsa_tx_sign


class ScriptSig(Script):
    """
    """
    def __init__(self):
        super().__init__()


class P2PKH(ScriptSig):
    """
    Basic pay-to-public-key-hash scriptsig.
    Implemented following the specification in :
    https://en.bitcoin.it/wiki/Transaction#Pay-to-PubkeyHash
    Args:
        _input (TxInput): Input related to that script
        _hashcode (): the hashcode that specefies which signature to do
        _signature (bytes): ecdsa signature for the input and transaction
    """
    __slots__ = ["_input", "_hashcode", "_signature"]

    def __init__(self, tx_input):
        self._input = tx_input
        self._hashcode = Types.signhash_all
        self._signature = bytes()

    def _build(self, pub):
        """
        Sets the data values with the proper signature once it's done and the
        public key where the btc's go

        Args:
            pub (): pubkey in hex format
        """
        # <signature> <pub_key>
        self._data = [StackDataField(self._signature), StackDataField(pub)]

    def sign(self, key):
        """
        Due to there's needed a signature, this is the class where the sign
        method should be. Already not decided how to implement that.

        Args:
            key (): private key to sign the transaction related to that script
            specified in hex.
        """
        pub = privkey_to_pubkey(key)
        address = pubkey_to_address(pub)
        idx = self._input.tx.inputs.index(self._input)

        serialized_tx = self._input.tx.serialize()
        tx = deserialize(serialized_tx)
        tx = signature_form(tx, idx, mk_pubkey_script(address), self._hashcode)

        self._signature = ecdsa_tx_sign(tx, key, self._hashcode)
        self._build(pub)

    @property
    def hashcode(self):
        return self._hashcode

    @hashcode.setter
    def hashcode(self, hashcode):
        """ Sets the hashcode to specify how the signature is done. """
        # Update values
        self._hashcode = hashcode


class P2SH(ScriptSig):
    """
    """
    __slots__ = ["_reedemScript"]

    def __init__(self, reedemScript):
        self._reedemScript = reedemScript
        self._build()

    def _build(self):
        # Signature(s)
        while 1:
            self._data.append(StackDataField())
        self._data.append(StackDataField(self._reedemScript))

    def sign(self):
        """
        Due to there's needed a signature, this is the class where the sign
        method should be. Already not decided how to implement that.
        """
        pass
