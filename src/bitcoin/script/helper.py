""" Methods to make scripting stuff easier """
import copy
from .sig import ScriptSig
from .hashcodes import Types
from .pubkey import P2PKH
from .. import address
from bitcoin.main import ecdsa_raw_sign
from bitcoin.transaction import der_encode_sig, bin_txhash, ecdsa_tx_sign
from hashlib import sha256
from ..field.general import VarInt


def electrum_sig_hash(message):
    """
    Calculates the magic hash of the transaction in order to sign it, don't ask
    for the message before the transaction, call it magic.

    Args:
        message(bytes): message to calculate the magic hash

    Returns:
        bytes: the double-sha256 hash of the message with the padding
        calculated properly
    """
    padded = b"\x18Bitcoin Signed Message:\n" + \
        VarInt(len(message)).serialize() + message
    return doublesha256(padded)


def doublesha256(value):
    """
    Given a value in bytes, calculates its double-sha256 and returns it

    Args:
        value (bytes): bytes to calculate the checksum against

    Returns:
        bytes: double sha256 checksum
    """
    # Check checksum
    return sha256(sha256(value).digest()).digest()


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

        script_to_pay = P2PKH()
        script_to_pay.address = addr

        newtx.inputs[idx].script = script_to_pay

    else:
        raise NotImplementedError("Not implemented yet, we're not so fast.")

    return newtx


def sign_tx(tx, priv_key, hashcode=None):
    # SECP256k1 is the Bitcoin elliptic curve
    # Creation of the key
    wif_address = address.WIF()
    wif_address.decode(priv_key)
    # Signature
    sig = ecdsa_tx_sign(tx.serialize(), priv_key)
    result = bytes().fromhex(sig)

    return result
