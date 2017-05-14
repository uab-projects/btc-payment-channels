# Libraries
import sys
from ..bitcoin.tx import SignableTx
from ..bitcoin.io.input import TxInput
from ..bitcoin.io.output import TxOutput
from ..bitcoin import script
from ..bitcoin import address
from ..bitcoin.script import redeem, pay
from ..bitcoin.field.opcode import OP_CS
from ..bitcoin.field.script import StackDataField


if __name__ == "__main__":
    # Transaction fields
    utxo_id = bytes().fromhex(
        "8f54e3adb8a2e34f9df1d2dcd41af8946c364e24dc70f64575966c4e93552206")
    utxo_num = 0
    utxo_value = 0.99637703
    fees = 0.0009
    to_pay = utxo_value - fees

    keys_num = len(sys.argv) - 2
    keys_multisig_num = keys_num - 1
    keys_base58 = sys.argv[2:]
    selection = int(sys.argv[1])
    keys = [address.WIF.decode(key) for key in keys_base58]
    keys_multisig = keys[1:]
    key_p2pkh = keys[0]

    # Create transaction to send funds to a multisig expiring P2SH
    transaction = SignableTx()

    unlocked_script = redeem.MultiSig(keys_multisig_num)
    tl_script = script.Script([StackDataField(key_p2pkh.public_key), OP_CS])
    # Redeem script
    redeem_script = redeem.TimeLockedScript(
        unlocked_script=unlocked_script,
        timelocked_script=tl_script,
        locktime=1123183
    )
    # Fill multisig
    for key in keys_multisig:
        unlocked_script.add_public_key(key.public_key)
    unlocked_script._build()

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

    # ==========================================================================
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
        redeem_script, pay_script), sequence=0xfffffffe))

    # Add outputs
    redeem_tx.add_output(
        TxOutput(to_pay_addr.script, btc=to_pay))

    # Pay script
    # How are we spending?
    pay_script.selection = selection

    # # Normal conditions
    if selection == 0:
        # # Multisig
        # # Add signatures
        pay_script.script = pay.MultiSig(redeem_script)
        for key in keys_multisig:
            pay_script.script.add_signature(redeem_tx.sign(
                key.private_key, 0, redeem_script))
    else:
        # # Normal checksig
        # # Add signature
        signature = redeem_tx.sign(key_p2pkh.private_key, 0, redeem_script)
        pay_script.script = script.Script([StackDataField(signature)])

    # Get transaction
    print(redeem_tx)
    print(redeem_tx.serialize().hex())
