"""
Defines the modules necessary to build Bitcoin scripts to be used in inputs
(scriptSig) and outputs (scriptPubKey)
"""
# Libraries
# # App
from .model import Script, TxInputOutputScript
from .pay import PayScript, MultiSig as MultiSigPayScript, \
                 TimeLockedScript as TimeLockedPayScript
from .pubkey import ScriptPubKey, P2PKH as P2PKHPubKeyScript, \
                    P2SH as P2SHPubKeyScript
from .redeem import RedeemScript, MultiSig as MultiSigRedeemScript, \
                    TimeLockedScript as TimeLockedRedeemScript
from .sig import ScriptSig, P2PKH as P2PKHScriptSig, P2SH as P2SHScriptSig

# Exports
__all__ = ["Script", "TxInputOutputScript", "PayScript", "MultiSigPayScript",
           "TimeLockedPayScript", "ScriptPubKey", "P2PKHPubKeyScript",
           "P2SHPubKeyScript", "RedeemScript", "MultiSigRedeemScript",
           "TimeLockedRedeemScript", "ScriptSig", "P2PKHScriptSig",
           "P2SHScriptSig"]
