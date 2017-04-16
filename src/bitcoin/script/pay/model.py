"""
Models a PaymentScript used in P2SH
"""
# Libraries
from ..general import Script


class PayScript(Script):
    """
    """
    __slots__ = ["_redeem"]

    def __init__(self, redeem):
        """ Creates a payment script given its redeem script to pay to """
        super().__init__()
        self._redeem = redeem
