""" Trying to create a transaction, validation of all the parts involved """

import sys
from ..bitcoin.tx import Tx
from ..bitcoin.io.input import TxInput
from ..bitcoin.io.output import p2pkh
from ..bitcoin.script.sig import P2PKH


if __name__ == "__main__":
    key = sys.argv[1]

    # Input data
    tx_id = bytes().fromhex("192b1a770e62c46474bec5195f73698a1b991fe6f6d262af43f45ec12080671b")
    tx_n = 0

    # Output data
    amount = 25
    value = 2.5
    fees = 0.0001
    value_return = amount - value - fees
    address_rcv = "mvgL4DJvQmyvvqh6BrtkP2GEqFJExK5DA3"
    address_return = "n3uGGXzpcrVggRVmhSr4c5pM3Y3DM4D9mP"

    # Attempting to create a P2PKH Transaction to the testnet
    transaction = Tx()

    # Add outputs
    out_0 = p2pkh(value, address_rcv)
    transaction.add_output(out_0)
    out_1 = p2pkh(value_return, address_return)
    transaction.add_output(out_1)

    # Add input
    in_0 = TxInput(tx_id, tx_n)
    transaction.add_input(in_0)
    print("Tx before sign", transaction)

    scriptsig = P2PKH(in_0)
    scriptsig.sign(key)

    print("Tx after sign", transaction)
    print(transaction.serialize().hex())
