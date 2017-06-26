"""
Defines the class and all the things needed to open a payment channel following
the Lightning Network specification
"""

from ....bitcoin import SignableTx, TxInput, TxOutput, MultiSigRedeemScript,\
                          TimeLockedRedeemScript, ScriptNum, ScriptData, \
                          Script, OP_CS, P2SHAddress, \
                          P2PKHScriptSig


def opening(keys):
    """
    Creates the transaction filling all the fields for the opening Transaction
    in order to create the Lightning Network
    """
    # SCENARIO: ALICE CREATES THE CHANNEL
    # Constants
    utxo_id = bytes().fromhex(
        "8dc10f058a0c6ee6ba481cfdb8cd350a5b406f76a024cdcbd96a87931372cb46")
    utxo_num = 0
    utxo_value = 1.00005
    fees = 0.00005
    to_pay = utxo_value - fees

    keyAlice = keys[0]
    keyBob = keys[1]

    keys_multisig_num = 2
    lock_time_value = 1123520

    # CREATION
    transaction = SignableTx()
    lock_time = ScriptNum(lock_time_value)
    # spending anytime with multisig
    unlocked_script = MultiSigRedeemScript(keys_multisig_num)
    # after specified time, Alice would spend with its own private key: refund
    # for simplicy same where the funds came from.
    tl_script = Script([ScriptData(keyAlice.public_key), OP_CS])

    # Redeem script
    redeem_script = TimeLockedRedeemScript(
        unlocked_script=unlocked_script,
        timelocked_script=tl_script,
        locktime=lock_time.value
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
    in0.script.input = in0
    transaction.add_input(in0)
    # transaction.add_input(in1)

    # CREATE THE OUTPUTS
    redeem_address = P2SHAddress(redeem_script)
    out0 = TxOutput(redeem_address.script, btc=to_pay)

    transaction.add_output(out0)

    # ADD SIGNATURES
    # Alice signature
    transaction.inputs[0].script.sign(keyAlice.private_key)
    # Bob Signature
    # transaction.inputs[1].script.sign(keyBob)

    # Returns the opening transaction
    return transaction, redeem_script
