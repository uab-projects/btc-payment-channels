""" Defines a base class to create OP_CODES in scripts and defines all the used
OP_CODES instances in the application """

from ..interfaces import Serializable

class OpCode(Serializable):
    """
    Defines a Bitcoin OP_CODE
    """
    __slots__ = ["_value"]

    def __init__(self, val):
        self._value = val

    def serialize(self):
        return bytes([self._value])

    def deserialize(self, value):
        self._value = value[0]
        return self

OP_0 = type('OP_0', (OpCode), {
    "name": "OP_0",
    "description": "An empty array of bytes is pushed onto the stack. (This is "
                   "not a no-op: an item is added to the stack.)"
})(0)

OP_2 = type('OP_2', (OpCode), {
    "name": "OP_2",
    "description": "The number in the word name (2) is pushed onto the stack."
})(82)

OP_PUSHDATA1 = type('OP_PUSHDATA1', (OpCode), {
    "name": "OP_PUSHDATA1",
    "description": "The next byte contains the number of bytes to be pushed "
                   "onto the stack."
})(76)

OP_PUSHDATA2 = type('OP_PUSHDATA2', (OpCode), {
    "name": "OP_PUSHDATA2",
    "description": "The next two bytes contain the number of bytes to be "
                   "pushed onto the stack."
})(77)

OP_PUSHDATA4 = type('OP_PUSHDATA4', (OpCode), {
    "name": "OP_PUSHDATA4",
    "description": "The next four bytes contain the number of bytes to be "
                   "pushed onto the stack."
})(78)

OP_DUP = type('OP_DUP', (OpCode), {
    "name": "OP_DUP",
    "description": "Duplicates the top stack item."
})(118)

OP_EV = OP_EQUALVERIFY = type('OP_EQUALVERIFY', (OpCode), {
    "name": "OP_EQUALVERIFY",
    "description": "Same as OP_EQUAL, but runs OP_VERIFY afterward."
})(136)

OP_HASH160 = type('OP_HASH160', (OpCode), {
    "name": "OP_HASH160",
    "description": "The input is hashed twice: first with SHA-256 and then "
                   "with RIPEMD-160."
})(169)

OP_CODESEPARATOR = type('OP_CODESEPARATOR', (OpCode), {
    "name": "OP_CODESEPARATOR",
    "description": """All of the signature checking words will only match
    signatures to the data after the most recently-executed OP_CODESEPARATOR."""
})(169)

OP_CS = OP_CHECKSIG = type('OP_CHECKSIG', (OpCode), {
    "name": "OP_CHECKSIG",
    "description": "The entire transaction's outputs, inputs, and script (from "
                   "the most recently-executed OP_CODESEPARATOR to the end) "
                   "are hashed. The signature used by OP_CHECKSIG must be a "
                   "valid signature for this hash and public key. If it is, 1 "
                   "is returned, 0 otherwise."
})(172)

OP_CMS = OP_CHECKMULTISIG = type('OP_CHECKMULTISIG', (OpCode), {
    "name": "OP_CHECKMULTISIG",
    "description": "Compares the first signature against each public key until "
                   "it finds an ECDSA match. Starting with the subsequent "
                   "public key, it compares the second signature against each "
                   "remaining public key until it finds an ECDSA match. The "
                   "process is repeated until all signatures have been checked "
                   "or not enough public keys remain to produce a successful "
                   "result. All signatures need to match a public key. Because "
                   "public keys are not checked again if they fail any "
                   "signature comparison, signatures must be placed in the "
                   "scriptSig using the same order as their corresponding "
                   "public keys were placed in the scriptPubKey or 2 "
                   "redeemScript. If all signatures are valid, 1 is returned, "
                   "0 otherwise. Due to a bug, one extra unused value is "
                   "removed from the stack."
})(174)
