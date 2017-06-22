"""
Defines the class and all the things needed to open a payment channel following
the Lightning Network specification
"""

from ......bitcoin import SignableTx, TxInput, TxOutput, MultiSigRedeemScript,\
                          TimeLockedRedeemScript, ScriptNum, ScriptData, \
                          Script, OP_HASH160, OP_CS, OP_EV, P2SHAddress, \
                          P2PKHScriptSig

from ......bitcoin.crypto.hash import ripemd160_sha256


def opening():
    """
    """
    # SCENARIO: ALICE CREATES THE CHANNEL
    # Constants
    utxo_id = bytes().fromhex(
        "")
    utxo_num = 0
    utxo_value = 1.00005
    fees = 0.00005
    to_pay = utxo_value - fees

    keyAlice = ""
    keyBob = ""
    keys_multisig_num = 2
    lock_time_value = 1123520

    # CREATION
    transaction = SignableTx()
    lock_time = ScriptNum(lock_time_value)

    # spending anytime with multisig
    unlocked_script = MultiSigRedeemScript(keys_multisig_num)
    # after specified time, Alice would spend with its own private key: refund
    tl_script = Script([ScriptData(keyAlice.public_key), OP_CS])

    # Redeem script
    redeem_script = TimeLockedRedeemScript(
        unlocked_script=unlocked_script,
        timelocked_script=tl_script,
        locktime=lock_time
    )
    # Add keys for multisig script
    keys_multisig = [keyAlice, keyBob]
    for key in keys_multisig:
        unlocked_script.add_public_key(key.public_key)
    unlocked_script._build()

    # CREATE THE INPUTS
    # Alice Funds
    in0 = TxInput(utxo_id, utxo_num, P2PKHScriptSig())
    # Bob funds
    # in1 = TxInput(utxo_id, utxo_num, P2PKHScriptSig())

    transaction.add_input(in0)
    # transaction.add_input(in1)

    # CREATE THE OUTPUTS
    redeem_address = P2SHAddress(redeem_script)
    out0 = TxOutput(redeem_address, btc=to_pay)

    transaction.add_output(out0)

    # ADD SIGNATURES
    # Alice signature
    transaction.inputs[0].script.sign(keyAlice)
    # Bob Signature
    # transaction.inputs[1].script.sign(keyBob)

    # Returns the opening transaction
    return transaction, redeem_script


def commitment(prev_tx_id=None, prev_redeem_script=None):
    """
    """
    # SCENARIO: ALICE PAYS BOB
    pass
    # Constants
    utxo_num = 0
    utxo_value = 1
    fees = 0.00005
    to_pay = utxo_value - fees
    to_return = utxo_value - to_pay

    lock_time_value = 1123520
    hash_val = "test"
    keyAlice = ""
    keyBob = ""
    selection = 0

    # Creation
    transaction = SignableTx()
    lock_time = ScriptNum(lock_time_value)
    hash_val = ripemd160_sha256(str.encode(hash_val))

    unlocked_script = Script([OP_HASH160, ScriptData(hash_val), OP_EV,
                              ScriptData(keyBob.public_key), OP_CS])
    tl_script = Script([ScriptData(keyAlice.public_key), OP_CS])

    redeem_script = TimeLockedRedeemScript(
        unlocked_script=unlocked_script,
        timelocked_script=tl_script,
        locktime=lock_time
    )

    # Create the inputs
    pay_script = prev_redeem_script.pay_script
    in0 = TxInput(prev_tx_id, utxo_num, pay_script)

    transaction.add_input(in0)

    # Create the outputs
    # Payment to Bob
    out0 = TxOutput(keyBob.p2pkh, btc=to_pay)
    transaction.add_output(out0)
    # Returns to her
    redeem_address = P2SHAddress(redeem_script)
    out1 = TxOutput(redeem_address, btc=to_return)
    transaction.add_output(out1)

    pay_script.selection = selection

    # SPENDING
    if selection == 0:
        # Bob, with the pre-image of the hash can spend
        signature = transaction.sign(keyBob.private_key, 0, redeem_script)
        pay_script.script = Script([ScriptData(signature)],
                                   ScriptData[hash_val])
    else:
        # Alice after a time can spend her money
        transaction.locktime = lock_time_value
        signature = transaction.sign(keyAlice.private_key, 0, redeem_script)
        pay_script.script = Script([ScriptData(signature)])

    # Add signature
    transaction.inputs[0].script.sign(keyAlice)
    transaction.inputs[0].script.sign(keyBob)

    # Returns the transaction
    return transaction


if __name__ == "__main__":
    tx, redeem_script = opening()
    upd_tx = commitment(tx.id, redeem_script)

    print("Opening transaction")
    print(tx)
    print(tx.serialize().hex())

    print("Alice creates the transaction, Bob could have done the same, \
            mirroring.")
    print(upd_tx)
    print(upd_tx.serialize().hex())
