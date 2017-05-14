"""
Models a PaymentScript used in P2SH
"""
# Libraries
from ..general import Script


class PayScript(Script):
    """
    A PayScript contains the data to spend a RedeemScript
    """
    __slots__ = ["_redeem"]

    def __init__(self, redeem):
        """ Creates a payment script given its redeem script to pay to """
        super().__init__()
        self._redeem = redeem

    def _build(self):
        """
        Builds the redeem script
        """
        raise NotImplementedError("You must implement this")

    def serialize(self):
        """
        Builds the redeem script and serializes it
        """
        self._build()
        return super().serialize()
