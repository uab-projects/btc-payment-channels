from .model import PayScript
from ...field.opcode import OP_0
from ...field.script import ScriptData


class MultiSig(PayScript):
    """
    """
    __slots__ = ["_signatures"]

    def __init__(self, redeem):
        super().__init__(redeem)
        self._signatures = []

    def add_signature(self, sign):
        """
        Adds a signature ot the script
        Args:
            sign(bytes): signature to append to the list of signatures
        """
        self._signatures.append(sign)

    def _build(self):
        """
        """
        self._data = []
        self._data.append(OP_0)
        for sign in self._signatures:
            self._data.append(ScriptData(sign))
