"""
Models a P2PKH scriptSig script, autobuilding the necessary opcodes to create
the P2PKH
"""
# Libraries
from .model import ScriptSig
from ...field.script import StackDataField
from ..hashcodes import Types
from ..helper import sign_tx, prepare_tx_to_sign
from ... import address
from ...address.helper import ripemd160_sha256
from bitcoin import main as buter
from bitcoin import transaction
from .. import pubkey


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
    __slots__ = ["_input", "_hashcode", "_signature", "_pubkey"]

    def __init__(self, tx_input):
        super().__init__()
        self._input = tx_input
        self._input.script = self
        self._hashcode = Types.sighash_all
        self._signature = bytes()
        self._pubkey = bytes()

    def _build(self):
        """
        Sets the data values with the proper signature once it's done and the
        public key where the btc's go

        Args:
            pub (): pubkey in hex format
        """
        # <signature> <pub_key>
        self._data = [StackDataField(self._signature),
                      StackDataField(self._pubkey)]

    def sign(self, key):
        """
        Due to there's needed a signature, this is the class where the sign
        method should be. Already not decided how to implement that.

        Args:
            key (): private key to sign the transaction related to that script
            specified in hex.
        """
        pub = buter.privkey_to_pubkey(key)
        idx = 0  # self._input.tx.inputs.index(self._input)
        addr = address.P2PKH()
        addr.pkh = ripemd160_sha256(bytes().fromhex(pub))
        tx = self._input.tx
        script_to_pay = pubkey.P2PKH()
        script_to_pay.address = addr
        tx = prepare_tx_to_sign(tx, idx, addr, self._hashcode)
        print("======== Tx to sign ========")
        print(tx)
        print(tx.serialize().hex())
        print("======== Tx to sign according to vButerin ======")
        tx_form_vbuter = transaction.signature_form(
            tx.serialize(), 0, tx.inputs[0].script.serialize(),
            0x01)
        print(tx_form_vbuter.hex())
        print("======== RESULT: %s" %
              "They match" if tx_form_vbuter == tx.serialize()
              else "Error, they don't match")
        self._signature = sign_tx(tx, key)
        self._pubkey = bytes().fromhex(pub)
        self._build()
        print("======== Tx signed ========")
        print(self._input.tx)
        print(self._input.tx.serialize().hex())
        print("======== Tx signed according to vButerin ======")
        tx_sign_vbuter = transaction.sign(
            self._input.tx.serialize().hex(), 0, key)
        print(tx_sign_vbuter)
        print("======== RESULT: %s" %
              "They match" if tx_sign_vbuter == self._input.tx.serialize()
              else "Error, they don't match")

    @property
    def hashcode(self):
        return self._hashcode

    @hashcode.setter
    def hashcode(self, hashcode):
        """ Sets the hashcode to specify how the signature is done. """
        # Update values
        self._hashcode = hashcode

    def __str__(self):
        """
        Returns the scriptSig in a printable way
        """
        return "<signature=%s> <pubkey=%s>" % \
            (self._signature.hex(), self._pubkey.hex())
