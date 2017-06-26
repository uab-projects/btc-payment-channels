"""
Interface for reedem scripts used in P2SH modes
"""
# Libraries
# # Builtin
from abc import abstractmethod
# # App
from ..pay import PayScript
from ...crypto.hash import ripemd160_sha256
from ..model import TxInputOutputScript


class RedeemScript(TxInputOutputScript):
    """
    Models a general reedem script, allowing to hash it to include it in a
    P2SH address
    """
    def __init__(self, data=None):
        """
        Initializes the redeem script with the given data
        """
        super().__init__(data)

    @property
    @abstractmethod
    def pay_script(self):
        """ Creates a payment script to pay this redeem script """
        return PayScript(self)

    @property
    def hash(self):
        """
        Hashes the reedemScript to be able to include this hash in a P2SH
        address.

        This means, take the script as bytes and then perform over the result
        the following hash operations:
        hash = ripemd160(sha256(script_bytes))

        Returns:
            bytes: hash
        """
        return ripemd160_sha256(self.serialize())
