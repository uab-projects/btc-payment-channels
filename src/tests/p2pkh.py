"""
Test a P2PKH transaction creation
"""
# Libraries
import sys
from ..bitcoin.tx import SignableTx
from ..bitcoin.io.input import TxInput
from ..bitcoin.io.output import TxOutput
from ..bitcoin import script
from ..bitcoin import address


if __name__ == "__main__":
    # Transaction fields
    utxo_id = bytes().fromhex(
        "258fb211724412d6ec6a531973c58233143e6ab355623658adc3164a5c70bd5b")
    utxo_n = 0
    utxo_value = 1.36650488
    fees = 0.001
    to_val = utxo_value - fees
    to_addr = "mmffw54dJ4SGC3PtSnAJpCtappy779agPV"
    key = sys.argv[1]

    # Create transaction
    transaction = SignableTx(
        inputs=[TxInput(utxo_id, utxo_n, script.sig.P2PKH())],
        outputs=[TxOutput(address.P2PKH.decode(to_addr).script, btc=to_val)]
    )
    transaction.inputs[0].script.sign(address.WIF.decode(key).private_key)
    print(transaction)
    print(transaction.serialize().hex())
