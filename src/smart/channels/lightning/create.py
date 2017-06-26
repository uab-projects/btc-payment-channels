"""
Defines the class and all the things needed to open a payment channel following
the Lightning Network specification
"""
import sys
from ....bitcoin import SignableTx, TxInput, TxOutput, MultiSigRedeemScript,\
                          TimeLockedRedeemScript, ScriptNum, ScriptData, \
                          Script, OP_HASH160, OP_CS, OP_EV, P2SHAddress, \
                          P2PKHScriptSig, WIFAddress, P2PKHAddress, \
                          P2SHScriptSig

from ....bitcoin.crypto.hash import ripemd160_sha256


def decodeKeys(keys_list):
    keys_decoded = []
    for key in keys_list:
        keys_decoded.append(WIFAddress.decode(key))

    return keys_decoded


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


def commitment(keys, prev_tx_id=None, redeem_multi=None, selection=0):
    """
    Creates the transaction filling all the fields for updating the balances in
    the Lightning Network
    """
    # SCENARIO: ALICE PAYS BOB
    # Constants
    utxo_num = 0
    utxo_value = 1
    fees = 0.00005
    to_pay = utxo_value - fees
    to_return = utxo_value - to_pay

    lock_time_value = 1123520
    hash_val = "test"
    keyAlice = keys[0]
    keyBob = keys[1]

    # Creation
    transaction = SignableTx()

    # Create the inputs
    pay_script = redeem_multi.pay_script
    pay_script.selection = selection  # multisig

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

    pay_script.selection = selection

    # SPENDING
    if selection == 0:
        signature = transaction.sign(keyBob.private_key, 0, redeem_multi)
        pay_script.script = Script([ScriptData(signature),
                                   ScriptData(hash_val)])
    else:
        # Multisig case
        transaction.locktime = lock_time_value
        signatureAlice = transaction.sign(keyAlice.private_key, 0,
                                          redeem_multi)
        signatureBob = transaction.sign(keyBob.private_key, 0, redeem_multi)

        pay_script.script = Script([ScriptData(signatureAlice),
                                   ScriptData(signatureBob)])

    # Returns the transaction and its redeem script
    return transaction, redeem_tricky


if __name__ == "__main__":
    # Read args
    sel = int(sys.argv[1])

    keys = sys.argv[2:]
    keys_decoded = decodeKeys(keys)

    tx, redeem_multi = opening(keys_decoded)

    print("Opening transaction")
    print(tx)
    print(tx.serialize().hex())

    upd_tx, redeem_tricky = commitment(keys_decoded, tx.id, redeem_multi,
                                       selection=sel)
    print("Alice creates the transaction, Bob could have done the same, \
            mirroring.")
    print(redeem_tricky)
    print(upd_tx)
    print(upd_tx.serialize().hex())
