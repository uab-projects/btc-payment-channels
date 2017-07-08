"""
Defines a base class to create OP_CODES in scripts and defines all the used
OP_CODES instances in the application
"""
# Libraries
from .model import Field


class Opcode(Field):
    """
    Defines a Bitcoin OP_CODE interface
    """
    def serialize(self):
        return bytes([self._value])

    @classmethod
    def deserialize(cls, value):
        return cls(value[0])

    def __str__(self):
        return self.name


# Constants
# Opcodes that mean push the following bytes to the stack
OP_PUSHDATA_MIN = 0x01
"""
    int: when represented as a byte, all numbers from this value to
    OP_PUSHDATA_MAX, the opcode means push this number of bytes into the stack.
"""
OP_PUSHDATA_MAX = 0x4b
"""
    int: when represented as a byte, all numbers from OP_PUSHDATA_MAX to
    this value, the opcode means push this number of bytes into the stack.
    Therefore, if you want to push more than this number of bytes to the stack
    you have to use other opcodes, the OP_PUSHDATA[1-4]
"""
OP_PUSHDATA_MAX_BYTES = 2**(2**4)
"""
    int: maximum value of bytes that can be pushed into the stack, knowing
    that the maximum bytes to set to be pushed into the stack are 4, using
    OP_PUSHDATA4
"""

OP_N_MIN = 0
"""
    int: minimum number whose opcode pushes that number to the stack
"""
OP_N_MAX = 16
"""
    int: maximum number whose opcode pushes that number to the stack
"""
OP_N_BASE = 80
"""
    int: the base of OP_1 -> OP_N_MAX opcode number
        (OP_1=OP_N_BASE+1, OP_2 = OP_N_BASE+2, ...)
"""

# Opcode definitions
OP_0 = OP_FALSE = type('OP_0', (Opcode,), {
    "name": "OP_0",
    "description": """An empty array of bytes is pushed onto the stack. """
                   """(This is not a no-op: an item is added to the stack.)"""
})(0)

OP_1 = OP_TRUE = type('OP_1', (Opcode,), {
    "name": "OP_1",
    "description": """The number 1 is pushed onto the stack."""
})(OP_N_BASE + 1)

OP_2 = type('OP_2', (Opcode,), {
    "name": "OP_2",
    "description": "The number in the word name (2) is pushed onto the stack."
})(OP_N_BASE + 2)


# Methods
def get_op_code_n(n):
    """
    Given an integer n, greater or equal than 0 (OP_N_MIN) and less or equal
    than 16 (OP_N_MAX), returns the associated opcode that pushes that number
    into the stack.

    Asserts if n is not in range

    Args:
        n (int): integer to get opcode that pushes that integer to the stack to
    """
    assert OP_N_MIN <= n <= OP_N_MAX, "The number %d can't be pushed to " + \
        "the stack with a single opcode"
    if n == 0:
        return OP_0
    elif n == 1:
        return OP_1
    elif n == 2:
        return OP_2
    else:
        return type("OP_%d" % n, (Opcode,), {
            "name": "OP_%d" % n,
            "description": "The number %d is pushed onto the stack" % n
        })(OP_N_BASE + n)


OP_PUSHDATA1 = type('OP_PUSHDATA1', (Opcode,), {
    "name": "OP_PUSHDATA1",
    "description": """The next byte contains the number of bytes to be pushed
    onto the stack."""
})(76)

OP_PUSHDATA2 = type('OP_PUSHDATA2', (Opcode,), {
    "name": "OP_PUSHDATA2",
    "description": """The next two bytes contain the number of bytes to be
    pushed onto the stack."""
})(77)

OP_PUSHDATA4 = type('OP_PUSHDATA4', (Opcode,), {
    "name": "OP_PUSHDATA4",
    "description": """The next four bytes contain the number of bytes to be
    pushed onto the stack."""
})(78)

OP_IF = type('OP_IF', (Opcode,), {
    "name": "OP_IF",
    "description": """If the top stack value is not False, the statements are
    executed. The top stack value is removed."""
})(99)

OP_ELSE = type('OP_ELSE', (Opcode,), {
    "name": "OP_ELSE",
    "description": """If the preceding OP_IF or OP_NOTIF or OP_ELSE was not
    executed then these statements are and if the preceding OP_IF or OP_NOTIF
    or OP_ELSE was executed then these statements are not."""
})(103)

OP_ENDIF = type('OP_ENDIF', (Opcode,), {
    "name": "OP_ENDIF",
    "description": """Ends an if/else block. All blocks must end, or the
    transaction is invalid. An OP_ENDIF without OP_IF earlier is also invalid.
    """
})(104)

OP_DROP = type('OP_DROP', (Opcode,), {
    "name": "OP_DROP",
    "description": """Removes the top stack item."""
})(117)

OP_DUP = type('OP_DUP', (Opcode,), {
    "name": "OP_DUP",
    "description": """Duplicates the top stack item."""
})(118)

OP_OVER = type('OP_OVER', (Opcode,), {
    "name": "OP_OVER",
    "description": """Copies the second-to-top stack item to the top."""
})(120)

OP_EQUAL = type('OP_EQUAL', (Opcode,), {
    "name": "OP_EQUAL",
    "description": "Returns 1 if the inputs are exactly equal, 0 otherwise."
})(135)

OP_EV = OP_EQUALVERIFY = type('OP_EQUALVERIFY', (Opcode,), {
    "name": "OP_EQUALVERIFY",
    "description": """Same as OP_EQUAL, but runs OP_VERIFY afterward."""
})(136)

OP_HASH160 = type('OP_HASH160', (Opcode,), {
    "name": "OP_HASH160",
    "description": """The input is hashed twice: first with SHA-256 and then
    with RIPEMD-160."""
})(169)

OP_CODESEPARATOR = type('OP_CODESEPARATOR', (Opcode,), {
    "name": "OP_CODESEPARATOR",
    "description": """All of the signature checking words will only match
    signatures to the data after the most recently-executed OP_CODESEPARATOR"""
})(169)

OP_CS = OP_CHECKSIG = type('OP_CHECKSIG', (Opcode,), {
    "name": "OP_CHECKSIG",
    "description": """The entire transaction's outputs, inputs, and script (from
    the most recently-executed OP_CODESEPARATOR to the end) are hashed. The
    signature used by OP_CHECKSIG must be a valid signature for this hash and
    public key. If it is, 1 is returned, 0 otherwise."""
})(172)

OP_CMS = OP_CHECKMULTISIG = type('OP_CHECKMULTISIG', (Opcode,), {
    "name": "OP_CHECKMULTISIG",
    "description": """Compares the first signature against each public key until
    it finds an ECDSA match. Starting with the subsequent public key, it
    compares the second signature against each remaining public key until it
    finds an ECDSA match. The process is repeated until all signatures have
    been checked or not enough public keys remain to produce a successful
    result.
    All signatures need to match a public key. Because public keys are not
    checked again if they fail any signature comparison, signatures must be
    placed in the scriptSig using the same order as their corresponding
    public keys were placed in the scriptPubKey or 2 redeemScript. If all
    signatures are valid, 1 is returned, 0 otherwise.
    Due to a bug, one extra unused value is removed from the stack."""
})(174)

OP_CLTV = OP_CHECKLOCKTIMEVERIFY = type('OP_CHECKLOCKTIMEVERIFY', (Opcode,), {
    "name": "OP_CHECKLOCKTIMEVERIFY",
    "description": """Marks transaction as invalid if the top stack item is
    greater than the transaction's nLockTime field, otherwise script evaluation
    continues as though an OP_NOP was executed"""
})(177)
