""" Methods to make scripting stuff easier """
import copy
from .sig import ScriptSig
from .hashcodes import Types
from .pubkey import P2PKH
from ecdsa import SigningKey, SECP256k1
import hashlib


def prepare_tx_to_sign(tx, idx, pub_key,  hashcode=None):
    """
    Prepares the transation in order to sign it

    Args:
        tx (Tx): transaction to sign
        idx (int): index of the utxo in the previous transaction
        pub_key (): public key to pay
        hashcode (int): type of the signature to do
    """
    print("Transaction is: ", tx)
    if hashcode is None or hashcode == Types.sighash_all:
        newtx = copy.deepcopy(tx)

        print("The copy is: ", newtx)
        for inp in newtx.inputs:
            inp.script = ScriptSig()

        script_to_pay = P2PKH
        script_to_pay.address = pub_key
        newtx.inputs[idx].script = script_to_pay

    else:
        raise NotImplementedError("Not implemented yet, we're not so fast.")

    return newtx


def sign_tx(tx, priv_key, hashcode=None):
    # SECP256k1 is the Bitcoin elliptic curve
    # Creation of the key
    sk = SigningKey.from_string(priv_key, curve=SECP256k1,
                                hashfunc=hashlib.sha256)
    sig = sk.sign(tx.serialize())

    # Verification of the signature
    vk = sk.get_verifying_key()
    vk.verify(sig, tx.serialize())

    return sig
