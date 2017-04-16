"""
Interface for reedem scripts used in P2SH modes
"""
# Libraries
from abc import abstractmethod
from ..pay import PayScript
import hashlib
from ..general import Script


class RedeemScript(Script):
    """
    Models a general reedem script, allowing to hash it to include it in a
    P2SH address
    """
    def __init__(self):
        super().__init__()

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
        sha256 = hashlib.sha256(self.serialize()).digest()
        ripemd = hashlib.new("ripemd160")
        ripemd.update(sha256)
        return ripemd.digest()
