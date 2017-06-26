"""
Consumes the current channel state transaction
"""
from ....bitcoin import SignableTx, TxInput, TxOutput, ScriptData, Script, \
                          P2PKHAddress, P2SHScriptSig


def consume(keys, prev_tx_id=None, redeem_tricky=None, hash_val="",
            selection=0):
    # Constants
    utxo_num = 0
    utxo_value = 1
    fees = 0.00005
    to_pay = utxo_value - fees

    lock_time_value = 1123520
    keyAlice = keys[0]
    keyBob = keys[1]

    # CREATION
    transaction = SignableTx()

    # Create the inputs
    pay_script = redeem_tricky.pay_script
    pay_script.selection = selection  # multisig

    in0 = TxInput(prev_tx_id, utxo_num,
                  P2SHScriptSig(redeem_tricky, pay_script))
    in0.script.input = in0
    transaction.add_input(in0)

    # Create the outputs
    out0 = TxOutput(P2PKHAddress(keyAlice.public_key).script, btc=to_pay)
    transaction.add_output(out0)

    # SPENDING THE COMMITMENT TRANSACTION
    if selection == 0:
        # Bob's can spend with Alice's pre-image and its own signature
        # This should be done by Bob
        signatureBob = transaction.sign(keyBob.private_key, 0, redeem_tricky)
        pay_script.script = Script([ScriptData(signatureBob),
                                   ScriptData(str.encode(hash_val))])
    else:
        # Alice can spend after a while with its own signature
        transaction.locktime = lock_time_value
        transaction.inputs[0].sequence = 0xfffffffe
        signatureAlice = transaction.sign(keyAlice.private_key, 0,
                                          redeem_tricky)
        pay_script.script = Script([ScriptData(signatureAlice)])

    return transaction
