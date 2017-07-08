"""
Models a PaymentScript used in P2SH. Basically contains data to spend a
redeem script. Be careful if you don't include just data, because therefore
the transaction will be non-standard
"""
# Libraries
from ..model import Script


class PayScript(Script):
    """
    A PayScript contains the data needed to spend a RedeemScript
    """
    __slots__ = ["_redeem"]

    def __init__(self, redeem, data=None):
        """
        Creates a payment script given its redeem script to pay to and
        optionally some data to add to the payment script
        """
        super().__init__(data)
        self._redeem = redeem

    @property
    def redeem_script(self):
        """
        Returns the related redeem script
        """
        return self._redeem
