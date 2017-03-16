""" Methods to make scripting stuff easier """
import copy
from .sig import ScriptSig
from .hashcodes import Types
from .pubkey import P2PKH
from .. import address
from bitcoin.main import ecdsa_sign
from bitcoin import transaction
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

    # sig = transaction.sign(tx.serialize().hex(), 0, wif_address.private_key.hex(), 1)
    sig = ecdsa_sign(tx.serialize(), wif_address.private_key.hex())

    sig = base64.b64decode(sig)
    sig = sig + bytes(1)
    return sig


def attempt_sig(tx, priv_key, scriptpk, hashcode=None):
    sighash = SignatureHash()
