import sys
from ..bitcoin.tx import SignableTx
from ..bitcoin.io.input import TxInput
from ..bitcoin.io.output import TxOutput
from ..bitcoin import script
from ..bitcoin import address
from ..bitcoin.script import redeem

if __name__ == "__main__":

    # Transaction fields
    utxo_id = bytes().fromhex(
        "69670f310aae3830e510adcce745129d64a9282f32e562996a788632bf1d49da")
    utxo_num = 0
    utxo_value = 0.99817703
    fees = 0.0009
    to_pay = utxo_value - fees
    keys_num = len(sys.argv) - 1
    keys_multisig_num = keys_num - 1
    keys_base58 = sys.argv[1:]
    keys = [address.WIF.decode(key) for key in keys_base58]
    keys_multisig = keys[1:]
    key_p2pkh = keys[0]

    # Create transaction to send funds to a multisig P2SH
    transaction = SignableTx()

    # Redeem script
    redeem_script = redeem.MultiSig(keys_multisig_num, keys_multisig_num)
    for key in keys_multisig:
        redeem_script.add_public_key(key.public_key)
    redeem_script._build()

    # Add input
    transaction.add_input(TxInput(utxo_id, utxo_num, script.sig.P2PKH()))

    # Add outputs
    redeem_address = address.P2SH(redeem_script)
    transaction.add_output(TxOutput(redeem_address.script, btc=to_pay))

    # Sign
    transaction.inputs[0].script.sign(key_p2pkh.private_key)

    # Get transaction
    print(transaction)
    print(transaction.serialize().hex())

    # Return my funds bruh

    # Transaction fields
    utxo_id = transaction.id
    to_pay = to_pay - fees
    to_pay_addr = address.P2PKH(public_key=key_p2pkh.public_key)

    # Create transaction
    redeem_tx = SignableTx()

    # Pay script
    pay_script = redeem_script.pay_script

    # Add inputs
    redeem_tx.add_input(TxInput(utxo_id, utxo_num, script.sig.P2SH(
        redeem_script, pay_script)))

    # Add outputs
    redeem_tx.add_output(
        TxOutput(to_pay_addr.script, btc=to_pay))

    # Sign
    # # Add signatures
    for key in keys_multisig:
        pay_script.add_signature(redeem_tx.sign(
            key.private_key, 0, redeem_script))

    pay_script._build()
    # Get transaction
    print(redeem_tx)
    print(redeem_tx.serialize().hex())
