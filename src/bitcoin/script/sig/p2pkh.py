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
from bitcoin import transaction
from bitcoin import main as buter
from bitcoin import base58
from ..pubkey import P2PKH as scp2pkh


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
        super().__init__()
        self._input = tx_input
        self._input.script = self
        self._hashcode = Types.sighash_all
        self._signature = bytes()

    def _build(self, pub):
        """
        Sets the data values with the proper signature once it's done and the
        public key where the btc's go

        Args:
            pub (): pubkey in hex format
        """
        # <signature> <pub_key>
        self._data = [StackDataField(self._signature),
                      StackDataField(pub)]

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

        script_to_pay = scp2pkh()
        script_to_pay.address = addr
        print(script_to_pay.serialize().hex())
        print(transaction.deserialize(tx.serialize()))

        tx_buter = transaction.signature_form(tx.serialize(), 0, script_to_pay.serialize().hex())


        tx = prepare_tx_to_sign(tx, idx, addr, self._hashcode)



        print("===============================")
        print(tx)
        print(tx_buter)
        print("===============================")



        self._signature = sign_tx(tx, key)
        # is pubkey correct?

        print("pubkey hash we know",
               base58.decode("mm6ttcEZgXxi3HGGJeh3sgUzfWGEiotRdv")[1:-4].hex())
        print("pubkey hash address", addr.pkh.hex())
        print("my address", addr.encode())
        self._build(bytes().fromhex(pub))

    @property
    def hashcode(self):
        return self._hashcode

    @hashcode.setter
    def hashcode(self, hashcode):
        """ Sets the hashcode to specify how the signature is done. """
        # Update values
        self._hashcode = hashcode
