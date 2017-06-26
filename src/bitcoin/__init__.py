"""
Defines basic data-structures for Bitcoin in Python, hard-coded parameters in
order to fill those data-structures and methods to serialize and deserialize
all of them in order to create valid data for the Bitcoin cryptocurrency
protocol

The aim of this module is to provide a puzzle-friendly framework to compose
easily any Bitcoin transaction, specially tohse containing smart contracts
"""
# Libraries
# # Parameters
from .nets import Network, DEFAULT_NETWORK
from .units import BTC_PER_SATOSHI, btc_to_satoshi, satoshi_to_btc
# # Addresses
from .address import Address, P2PKH as P2PKHAddress, P2SH as P2SHAddress, \
                     WIF as WIFAddress, Types as AddressTypes
# # Fields
from .field import U2BLEInt, U4BLEInt, U8BLEInt, S4BLEInt, VarInt, \
                   VarLEChar, OP_0, OP_PUSHDATA_MIN, OP_PUSHDATA_MAX, \
                   OP_PUSHDATA_MAX_BYTES, OP_1, OP_2, OP_PUSHDATA1, \
                   OP_PUSHDATA2, OP_PUSHDATA4, OP_IF, OP_ELSE, OP_ENDIF, \
                   OP_DROP, OP_DUP, OP_OVER, OP_EQUAL, OP_EV, \
                   OP_EQUALVERIFY, OP_HASH160, OP_CODESEPARATOR, OP_CS, \
                   OP_CHECKSIG, OP_CMS, OP_CHECKMULTISIG, OP_CLTV, \
                   OP_CHECKLOCKTIMEVERIFY, get_op_code_n, ScriptData, \
                   ScriptNum
# # Transaction Input and Outputs
from .io import TxInputOutput, TxInput, TxOutput
# # Scripts
from .script import Script, TxInputOutputScript, PayScript, \
                    MultiSigPayScript, TimeLockedPayScript, ScriptPubKey, \
                    P2PKHPubKeyScript, P2SHPubKeyScript, RedeemScript, \
                    MultiSigRedeemScript, TimeLockedRedeemScript, ScriptSig, \
                    P2PKHScriptSig, P2SHScriptSig

# # Transactions
from .tx import SignableTx, BasicTx

# Exported items
__all__ = ["Network", "DEFAULT_NETWORK", "BTC_PER_SATOSHI", "btc_to_satoshi",
           "satoshi_to_btc", "Address", "P2PKHAddress", "P2SHAddress",
           "WIFAddress", "AddressTypes", "SignableTx", "BasicTx", "U2BLEInt",
           "U4BLEInt", "U8BLEInt", "S4BLEInt", "VarInt",
           "VarLEChar", "OP_0", "OP_PUSHDATA_MIN", "OP_PUSHDATA_MAX",
           "OP_PUSHDATA_MAX_BYTES", "OP_1", "OP_2", "OP_PUSHDATA1",
           "OP_PUSHDATA2", "OP_PUSHDATA4", "OP_IF", "OP_ELSE", "OP_ENDIF",
           "OP_DROP", "OP_DUP", "OP_OVER", "OP_EQUAL", "OP_EV",
           "OP_EQUALVERIFY", "OP_HASH160", "OP_CODESEPARATOR", "OP_CS",
           "OP_CHECKSIG", "OP_CMS", "OP_CHECKMULTISIG", "OP_CLTV",
           "OP_CHECKLOCKTIMEVERIFY", "get_op_code_n", "ScriptData",
           "ScriptNum", "Script", "TxInputOutputScript", "PayScript",
           "MultiSigPayScript", "TimeLockedPayScript", "ScriptPubKey",
           "P2PKHPubKeyScript", "P2SHPubKeyScript", "RedeemScript",
           "MultiSigRedeemScript", "TimeLockedRedeemScript", "ScriptSig",
           "P2PKHScriptSig", "P2SHScriptSig", "TxInputOutput", "TxInput",
           "TxOutput"]
