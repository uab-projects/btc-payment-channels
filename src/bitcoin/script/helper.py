""" Methods to make scripting stuff easier """
import copy
from .sig import ScriptSig
from .hashcodes import Types
from .pubkey import P2PKH
from .. import address
from ecdsa import SigningKey, SECP256k1
from bitcoin import base58
from bitcoin.main import ecdsa_sign


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
        pub_key_bytes = bytes().fromhex(pub_key)
        print(pub_key_bytes, len(pub_key_bytes))
        script_to_pay = P2PKH()
        script_to_pay.address = address.P2PKH.from_public_key(pub_key_bytes)
        newtx.inputs[idx].script = script_to_pay

    else:
        raise NotImplementedError("Not implemented yet, we're not so fast.")

    return newtx


def sign_tx(tx, priv_key, hashcode=None):
    # SECP256k1 is the Bitcoin elliptic curve
    # Creation of the key
    wif_address = address.WIF()
    wif_address.decode(priv_key)
    print(base58.decode(priv_key).hex())
    print(wif_address.value.hex())
    print(wif_address.private_key.hex())
    sig = ecdsa_sign(tx.serialize(), wif_address.private_key.hex())

    return sig
