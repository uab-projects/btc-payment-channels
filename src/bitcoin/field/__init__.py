"""
Defines several data structures used in low-level bitcoin for carrying data
in the protocol as fields in transactions, blocks...

Modules defined here are only used inside the app to provide easy storage and
serialization, it's not inteded to use for the app user. This way, this classes
provided here should only be used to create data structure that will deal with
Python data types and may use this classes just to store them, knowing that
they will also provide serialization methods.

The following modules allow to deal with low-level data providing methods to
easily handle the data in fields and providing methods to transform them into
an array of bytes compatible with the Bitcoin standards definition and
vice-versa

Modules and classes are added as needed so maybe many possible fields may exist
in the Bitcoin protocol but not available here because it's not used anywhere.
"""
# Libraries
# # App
from .general import U2BLEInt, U4BLEInt, U8BLEInt, S4BLEInt, VarInt, VarLEChar
from .opcode import OP_0, get_op_code_n, OP_PUSHDATA_MIN, OP_PUSHDATA_MAX, \
                    OP_PUSHDATA_MAX_BYTES, OP_1, OP_2, OP_PUSHDATA1, \
                    OP_PUSHDATA2, OP_PUSHDATA4, OP_IF, OP_ELSE, OP_ENDIF, \
                    OP_DROP, OP_DUP, OP_OVER, OP_EQUAL, OP_EV, \
                    OP_EQUALVERIFY, OP_HASH160, OP_CODESEPARATOR, OP_CS, \
                    OP_CHECKSIG, OP_CMS, OP_CHECKMULTISIG, OP_CLTV, \
                    OP_CHECKLOCKTIMEVERIFY, Opcode
from .script import ScriptData, ScriptNum

# Exports
__all__ = ["U2BLEInt", "U4BLEInt", "U8BLEInt", "S4BLEInt", "VarInt",
           "VarLEChar", "OP_0", "OP_PUSHDATA_MIN", "OP_PUSHDATA_MAX",
           "OP_PUSHDATA_MAX_BYTES", "OP_1", "OP_2", "OP_PUSHDATA1",
           "OP_PUSHDATA2", "OP_PUSHDATA4", "OP_IF", "OP_ELSE", "OP_ENDIF",
           "OP_DROP", "OP_DUP", "OP_OVER", "OP_EQUAL", "OP_EV",
           "OP_EQUALVERIFY", "OP_HASH160", "OP_CODESEPARATOR", "OP_CS",
           "OP_CHECKSIG", "OP_CMS", "OP_CHECKMULTISIG", "OP_CLTV",
           "OP_CHECKLOCKTIMEVERIFY", "Opcode", "get_op_code_n", "ScriptData",
           "ScriptNum"]
