"""
Methods to generate outputs easily, combining the TxOutput and script pubkeys
available
"""
# Libraries
from .model import TxOutput
from ... import address
from ... import script


def p2pkh(btc_value, btc_address):
    """
    Given a BTC address, generates a TxOutput with a P2PKH scriptPubKey that
    pays to the given btc_address

    Args:
        btc_value (float): value of the output in btc
        btc_address (str): the base58-encoded P2PKH address

    Returns:
        TxOutput: transaction output with the value and script set
    """
    pubkey = script.pubkey.P2PKH()
    pubkey.address = address.P2PKH().decode(btc_address)
    tx_output = TxOutput()
    tx_output.btc = btc_value
    tx_output.script = pubkey
    return tx_output
