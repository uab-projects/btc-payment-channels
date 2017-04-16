import sys
from bitcoin import main as vbuter
from ..bitcoin.tx import Tx
from ..bitcoin.io.input import TxInput
from ..bitcoin.io.output import TxOutput
from ..bitcoin import script
from ..bitcoin import address
from ..bitcoin.nets import Network
from ..bitcoin.script import redeem
from ..bitcoin.script.helper import prepare_tx_to_sign_multisig, sign_tx


if __name__ == "__main__":

    # Transaction fields
    prev_tx = bytes().fromhex("""40d271f31d4249e4c58a952348dff8f211b71edbf646086b1faf17561f0696f9""")
    prev_tx_out = 0
    utxo_value = 0.11000000
    fees = 0.00025
    to_pay = utxo_value - fees
    p2pkh_key, priv_key_0, priv_key_1 = sys.argv[1:4]
    pubkey_0 = vbuter.privkey_to_pubkey(priv_key_0)
    pubkey_1 = vbuter.privkey_to_pubkey(priv_key_1)

    # Create transaction
    transaction = Tx()

    rS = redeem.MultiSig(2, 2)
    rS.add_PubKey(bytes().fromhex(pubkey_0))
    rS.add_PubKey(bytes().fromhex(pubkey_1))
    rS._build()

    # Add outputs
    out_0 = TxOutput(script.pubkey.P2SH(address.P2SH(Network.testnet, rS)),
                     btc=to_pay)
    transaction.add_output(out_0)

    # Add input
    in_0 = TxInput(prev_tx, prev_tx_out)
    transaction.add_input(in_0)
    scriptsig = script.sig.P2PKH(in_0)
    scriptsig.sign(p2pkh_key)

    # Get transaction
    print(transaction)
    print(transaction.serialize().hex())

    # --------------------------------------------------------------------------
    # redeem the previous transaction
    # --------------------------------------------------------------------------

    # Transaction fields
    prev_tx = transaction.id
    to_pay = to_pay - fees
    to_pay_addr = "n1ExFff5BDJuZpySzLnd7L863VZMTFcj8X"
    pay_script = rS.pay_script

    # Create transaction
    redeem_tx = Tx()

    # Add outputs
    out_1 = TxOutput(script.pubkey.P2PKH(address.P2PKH.decode(to_pay_addr)),
                     btc=to_pay)
    redeem_tx.add_output(out_1)

    # Add inputs
    in_1 = TxInput(prev_tx, 0)
    redeem_tx.add_input(in_1)
    in_1.script = script.sig.P2SH(rS, pay_script)

    # Make signatures
    s_tx = prepare_tx_to_sign_multisig(redeem_tx, 0, out_0.script)
    sig_0 = sign_tx(s_tx, priv_key_0)
    sig_1 = sign_tx(s_tx, priv_key_1)
    # Add signatures
    pay_script.add_signature(sig_0)
    pay_script.add_signature(sig_1)
    pay_script._build()

    # Get transaction
    print(redeem_tx)
    print(redeem_tx.serialize().hex())
