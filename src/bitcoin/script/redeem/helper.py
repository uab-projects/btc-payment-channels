"""
"""
from ...field.opcode import OP_0, OP_2


def get_op_code_n(n):
    if n == 0:
        return OP_0
    if n == 2:
        return OP_2
    else:
        return False
