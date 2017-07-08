"""
Models a basic scriptSig. It has references to the transaction it belongs to
provide facilities for it's scripts to be appended signatures that require
therefore the transaction that has to be signed

More information could be found in:
https://bitcoin.org/en/developer-guide#standard-transactions
"""
# Libraries
# # App
from ..model import TxInputOutputScript


class ScriptSig(TxInputOutputScript):
    """
    Models a scriptSig script
    """
    def __init__(self, tx_input=None, data=None):
        """
        Initializes an scriptSig given the tx_input and data
        """
        super().__init__(tx_input, data)

    @property
    def input(self):
        """
        Returns the input the script sig belongs to
        """
        return self.parent

    @input.setter
    def input(self, new_input):
        """
        Sets the input the scriptSig belongs to
        """
        self.parent = new_input
