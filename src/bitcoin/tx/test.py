"""
Tests the Transaction model and methods
"""
# Libraries
from .model import BasicTx
from .sign import SignableTx
from ..io.input import TxInput
from ..io.output import TxOutput
from .. import address
from .. import script
from bitcoin.transaction import signature_form, mk_pubkey_script, \
                                SIGHASH_ALL, bin_txhash, der_encode_sig, \
                                ecdsa_tx_sign, sign
from bitcoin.main import ecdsa_raw_sign
from ..crypto import ecdsa


# Methods
def main():
    global signable_bytes, private_key
    print("Testing BasicTx class")
    print(" - Creating empty transaction")
    T_EMPTYTX = BasicTx()
    print(" - Serializing empty transaction")
    T_EMPTYTX_SER = T_EMPTYTX.serialize()
    print(" - Result of serialization:", T_EMPTYTX_SER.hex())
    print(" - Deserializing previous transaction")
    T_EMPTYTX_CPY = BasicTx.deserialize(T_EMPTYTX_SER)
    print(" - Result of deserialization...", end="")
    assert T_EMPTYTX_CPY == T_EMPTYTX, """failed deserialization test"""
    print("pass")
    print("Testing SignableTx class")
    print(" - Creating a sample transaction")
    wif = "5JGXXBdFs68dJuNSer4ZqdVQRRRR8MWALtYGrvzq61roZgZuUjA"
    wif_addr = address.WIF.decode(wif)
    private_key = wif_addr.private_key
    address_to = address.P2PKH(public_key=wif_addr.public_key).encode()
    tx = SignableTx()
    tx.add_input(TxInput(
        bytes().fromhex("258fb211724412d6ec6a531973c58233143e6ab355623658adc31"
                        + "64a5c70bd5b"),
        0, script.sig.P2PKH()))
    tx.add_output(TxOutput(address.P2PKH.decode(address_to).script, btc=10))
    tx.inputs[0].script.sign(
        private_key, address.P2PKH.decode(address_to).script)
    print(" - Creating signable transaction: ", end="")
    signable = tx.signable_tx(0, address.P2PKH.decode(address_to).script)
    vbuterin_signable = signature_form(
        tx.serialize().hex(), 0, mk_pubkey_script(address_to), SIGHASH_ALL)
    our_signable = signable.serialize().hex()
    assert vbuterin_signable == our_signable, \
        "Our signable transaction does not match Vitalik Buterin signable " + \
        "transaction: \nVitalik's:\n%s\nOurs:\n%s" % (
            vbuterin_signable, our_signable)
    print("pass")
    print(" - Creating hash of the signable transaction: ", end="")
    signable_bytes = signable.signable_hash()
    our_signable_bytes = signable_bytes.hex()
    vbuterin_signable_bytes = bin_txhash(vbuterin_signable, SIGHASH_ALL).hex()
    assert our_signable_bytes == vbuterin_signable_bytes, \
        "Our signable transaction hash does not match Vitalik Buterin " + \
        "signable transaction hash: \nVitalik's:\n%s\nOurs:\n%s" % (
            vbuterin_signable_bytes, our_signable_bytes)
    print("pass")
    print(" - Testing raw signatures: ", end="")
    vbuterin_signature = ecdsa_raw_sign(vbuterin_signable_bytes, private_key)
    our_signature = ecdsa.sign(signable_bytes, private_key)
    assert our_signature == vbuterin_signature, \
        "Our signature does not match Vitalik Buterin signature: " + \
        "\nVitalik's:\n%s\nOurs:\n%s" % (vbuterin_signature, our_signature)
    print("pass")
    print(" - Testing DER encode signatures: ", end="")
    vbuterin_der_signature = der_encode_sig(*vbuterin_signature)
    our_der_signature = ecdsa.der_sign(signable_bytes, private_key).hex()
    assert our_der_signature == vbuterin_der_signature, \
        "Our DER signature does not match Vitalik Buterin DER signature: " + \
        "\nVitalik's:\n%s\nOurs:\n%s" % (
            vbuterin_der_signature, our_der_signature)
    print("pass")
    print(" - Test complete signature: ", end="")
    vbuterin_signature_full = ecdsa_tx_sign(vbuterin_signable, private_key)
    our_signature_full = tx.sign(
        private_key, 0, address.P2PKH.decode(address_to).script).hex()
    assert our_signature_full == vbuterin_signature_full, \
        "Our tx signature does not match Vitalik Buterin tx signature: " + \
        "\nVitalik's:\n%s\nOurs:\n%s" % (
            vbuterin_signature_full, our_signature_full)
    print("pass")
    print(" - Test transaction signed: ", end="")
    vbuterin_tx_signed = sign(
        tx.serialize().hex(), 0, private_key.hex())
    our_tx_signed = tx.serialize().hex()
    assert our_tx_signed == vbuterin_tx_signed, \
        "Our tx signed does not match Vitalik Buterin tx signed: " + \
        "\nVitalik's:\n%s\nOurs:\n%s" % (
            vbuterin_tx_signed, our_tx_signed)
    print("pass")
    print(tx)


# Execute
if __name__ == "__main__":
    main()
