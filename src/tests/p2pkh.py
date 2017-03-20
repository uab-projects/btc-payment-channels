"""
Test a P2PKH transaction creation
"""
# Libraries
import sys
from ..bitcoin.tx import Tx
from ..bitcoin.io.input import TxInput
from ..bitcoin.io import output
from ..bitcoin import script


if __name__ == "__main__":
    # Transaction fields
    prev_tx = bytes().fromhex(
        "258fb211724412d6ec6a531973c58233143e6ab355623658adc3164a5c70bd5b")
    prev_tx_out = 0
    utxo_value = 1.36650488
    fees = 0.001
    to_val = utxo_value - fees
    to_addr = "mmffw54dJ4SGC3PtSnAJpCtappy779agPV"
    key = sys.argv[1]

    # Create transaction
    transaction = Tx()

    # Add outputs
    out_0 = output.p2pkh(to_val, to_addr)
    transaction.add_output(out_0)

    # Add input
    in_0 = TxInput(prev_tx, prev_tx_out)
    transaction.add_input(in_0)
    scriptsig = script.sig.P2PKH(in_0)
    scriptsig.sign(key)
    print(transaction)
    print(transaction.serialize().hex())
