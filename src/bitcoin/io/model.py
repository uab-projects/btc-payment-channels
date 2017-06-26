"""
Models what every input or output in a transaction has to have (a script)
"""
# Libraries
# # App
from ..interfaces import Serializable
from ..script import TxInputOutputScript


class TxInputOutput(Serializable):
    """
    Defines what every input and output must contain and implement

    Attributes:
        _script (Script): script to send the output to or to spend an input
        _tx (BasicTx): transaction the input / output belongs to
    """
    __slots__ = ["_tx", "_script"]

    def __init__(self, tx=None, script=None):
        """
        Initializes a new transaction input / output given it's script
        """
        self._tx = tx
        self._script = script

    @property
    def tx(self):
        """
        Returns the transaction where the input belongs
        """
        return self._tx

    @tx.setter
    def tx(self, new_tx):
        """
        Sets the script of the input / output

        Args:
            new_tx (BasicTx): transaction of the input
                              can be None to set no script
                              will update related transaction too
        """
        # Remove script assignment
        old_tx = self._tx
        self._tx = new_tx
        # Remove itself from previous tx
        if old_tx is not None:
            if self in old_tx.inputs:
                old_tx.inputs.remove(self)
            if self in old_tx.outputs:
                old_tx.outputs.remove(self)

    @property
    def script(self):
        """
        Returns the script of the input / output, if any
        """
        return self._script

    @script.setter
    def script(self, new_script):
        """
        Sets the script of the input / output

        Args:
            new_script (Script): script of the input / output
                             can be None to set no script
                             will also set the input / output of the script
                             as itself
        """
        # Remove script assignment
        old_script = self._script
        self._script = new_script
        # Remove itself from previous script
        if old_script is not None \
           and isinstance(old_script, TxInputOutputScript) \
           and old_script.parent == self:
            old_script.parent = None
        # Add itself to new script
        if new_script is not None \
           and isinstance(new_script, TxInputOutputScript) \
           and new_script.parent != self:
            new_script.parent = self
