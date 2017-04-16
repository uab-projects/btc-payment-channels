""" Methods to make scripting stuff easier """
import copy
from .sig import ScriptSig
from .hashcodes import Types
from .pubkey import P2PKH
from bitcoin.transaction import ecdsa_tx_sign


def prepare_tx_to_sign(tx, idx, addr,  hashcode=None):
    """
    Prepares the transation in order to sign it

    Args:
        tx (Tx): transaction to sign
        idx (int): index of the utxo in the previous transaction
        addr (Adress): public key hash to receive the money
        hashcode (int): type of the signature to do
    """
    if hashcode is None or hashcode == Types.sighash_all:
        newtx = copy.deepcopy(tx)
        for inp in newtx.inputs:
            inp.script = ScriptSig()

        script_to_pay = P2PKH(addr)

        newtx.inputs[idx].script = script_to_pay

    else:
        raise NotImplementedError("Not implemented yet, we're not so fast.")

    return newtx


def prepare_tx_to_sign_multisig(tx, idx, script,  hashcode=None):
    """
    Prepares the transation in order to sign it

    Args:
        tx (Tx): transaction to sign
        idx (int): index of the utxo in the previous transaction
        addr (Adress): public key hash to receive the money
        hashcode (int): type of the signature to do
    """
    if hashcode is None or hashcode == Types.sighash_all:
        newtx = copy.deepcopy(tx)
        for inp in newtx.inputs:
            inp.script = ScriptSig()

        newtx.inputs[idx].script = script

    else:
        raise NotImplementedError("Not implemented yet, we're not so fast.")

    return newtx


def sign_tx(tx, priv_key, hashcode=None):
    # SECP256k1 is the Bitcoin elliptic curve
    # Creation of the key
    sig = ecdsa_tx_sign(tx.serialize(), priv_key)
    return bytes().fromhex(sig)
