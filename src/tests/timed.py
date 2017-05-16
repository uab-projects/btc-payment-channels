# Libraries
import sys
import math
from ..bitcoin.tx import SignableTx
from ..bitcoin.io.input import TxInput
from ..bitcoin.io.output import TxOutput
from ..bitcoin import script
from ..bitcoin import address
from ..bitcoin.script import redeem, pay
from ..bitcoin.field.opcode import OP_CS
from ..bitcoin.field.script import ScriptData, ScriptNum


if __name__ == "__main__":
    # Transaction fields
    utxo_id = bytes().fromhex(
        "8dc10f058a0c6ee6ba481cfdb8cd350a5b406f76a024cdcbd96a87931372cb46")
    utxo_num = 0
    utxo_value = 0.99990000
    fees = 0.00005
    to_pay = utxo_value - fees

    # Param lecture
    keys_num = len(sys.argv) - 2
    keys_multisig_num = keys_num - 1
    keys_base58 = sys.argv[2:]
    selection = int(sys.argv[1])
    keys = [address.WIF.decode(key) for key in keys_base58]
    keys_multisig = keys[1:]
    key_p2pkh = keys[0]

    # Create transaction to send funds to a multisig expiring P2SH
    transaction = SignableTx()
    lock_time = ScriptNum(1123520)

    unlocked_script = redeem.MultiSig(keys_multisig_num)
    tl_script = script.Script([ScriptData(key_p2pkh.public_key), OP_CS])
    # Redeem script
    redeem_script = redeem.TimeLockedScript(
        unlocked_script=unlocked_script,
        timelocked_script=tl_script,
        locktime=lock_time
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
    utxo_num = 0
    to_pay = to_pay - fees
    to_pay_addr = address.P2PKH(public_key=key_p2pkh.public_key)

    lock_time = 1123500

    # Create transaction
    redeem_tx = SignableTx(locktime=lock_time)

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
        pay_script.script = script.Script([ScriptData(signature)])

    # Get transaction
    print(redeem_tx)
    print(redeem_tx.serialize().hex())
