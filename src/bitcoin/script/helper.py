""" Methods to make scripting stuff easier """
import copy
from .sig import ScriptSig
from .hashcodes import Types
from .pubkey import P2PKH
from .. import address
from bitcoin.main import ecdsa_raw_sign
from bitcoin.transaction import der_encode_sig
from ..address.helper import doublesha256_checksum
from ..field.general import VarInt
import base64
from bitcoin.core.script import SignatureHash


def prepare_tx_to_sign(tx, idx, pub_key,  hashcode=None):
    """
    Prepares the transation in order to sign it

    Args:
        tx (Tx): transaction to sign
        idx (int): index of the utxo in the previous transaction
        pub_key (): public key to pay
        hashcode (int): type of the signature to do
    """
    if hashcode is None or hashcode == Types.sighash_all:
        newtx = copy.deepcopy(tx)
        for inp in newtx.inputs:
            inp.script = ScriptSig()
        pub_key_bytes = bytes().fromhex(pub_key)

        script_to_pay = P2PKH()
        script_to_pay.address = address.P2PKH.from_public_key(pub_key_bytes)
        print(script_to_pay.serialize())
        newtx.inputs[idx].script = script_to_pay

    else:
        raise NotImplementedError("Not implemented yet, we're not so fast.")

    return newtx


def sign_tx(tx, priv_key, hashcode=None):
    # SECP256k1 is the Bitcoin elliptic curve
    # Creation of the key
    wif_address = address.WIF()
    wif_address.decode(priv_key)

    v, r, s = ecdsa_raw_sign(tx.serialize(), wif_address.private_key.hex())
    sig_hex = der_encode_sig(v, r, s)
    return bytes().fromhex(sig_hex)+b'\x01'


def electrum_sig_hash(message):
    padded = b"\x18Bitcoin Signed Message:\n" + \
        VarInt(len(message)).serialize() + message
    return doublesha256_checksum(padded)
