"""
Creates a transaction for updating the current channel state
"""
from ....bitcoin import SignableTx, TxInput, TxOutput, \
                          TimeLockedRedeemScript, ScriptNum, ScriptData, \
                          Script, OP_HASH160, OP_CS, OP_EV, P2SHAddress, \
                          P2PKHAddress, P2SHScriptSig, OP_0
from ....bitcoin.crypto.hash import ripemd160_sha256


def commitment(keys, prev_tx_id=None, redeem_multi=None, selection=0):
    """
    Creates the transaction filling all the fields for updating the balances in
    the Lightning Network
    """
    # SCENARIO: ALICE PAYS BOB
    # Constants
    utxo_num = 0
    utxo_value = 0.49995000
    fees = 0.00005
    to_pay = 0.4
    to_return = utxo_value - to_pay - fees

    lock_time_value = 1149120
    hash_val = "test"
    keyAlice = keys[0]
    keyBob = keys[1]

    # Creation
    transaction = SignableTx()

    # Create the inputs
    pay_script = redeem_multi.pay_script
    pay_script.selection = 0  # multisig

    in0 = TxInput(prev_tx_id, utxo_num,
                  P2SHScriptSig(redeem_multi, pay_script))
    in0.script.input = in0
    transaction.add_input(in0)

    # Create the outputs
    lock_time = ScriptNum(lock_time_value)
    hash_val = ripemd160_sha256(str.encode(hash_val))

    unlocked_script = Script([OP_HASH160, ScriptData(hash_val), OP_EV,
                              ScriptData(keyBob.public_key), OP_CS])
    tl_script = Script([ScriptData(keyAlice.public_key), OP_CS])

    redeem_tricky = TimeLockedRedeemScript(
        unlocked_script=unlocked_script,
        timelocked_script=tl_script,
        locktime=lock_time.value
    )

    # Payment to Bob
    out0 = TxOutput(P2PKHAddress(keyBob.public_key).script, btc=to_pay)
    transaction.add_output(out0)
    # Tricky output
    redeem_address = P2SHAddress(redeem_tricky)
    out1 = TxOutput(redeem_address.script, btc=to_return)
    transaction.add_output(out1)

    # SPENDING
    if selection:
        raise NotImplementedError("Only multisig spending allowed by the \
                                  moment.")
    else:
        # Multisig case
        signatureAlice = transaction.sign(keyAlice.private_key, 0,
                                          redeem_multi)
        signatureBob = transaction.sign(keyBob.private_key, 0, redeem_multi)

        pay_script.script = Script([OP_0, ScriptData(signatureAlice),
                                   ScriptData(signatureBob)])

    # Returns the transaction and its redeem script
    return transaction, redeem_tricky
