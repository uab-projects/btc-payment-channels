"""
Defines RedeemScripts that contain time conditions in order to spend funds
"""
# Libraries
# # App
from .model import RedeemScript


class TimeLockedScript(RedeemScript):
    """
    A time locked redeem script allows to set two scripts for spending an UTXO:
     - lifetime_script
        Script that will allow to spend the funds at any time
     - timelocked_script
        Script that will be allowed to spend after a certain period of time
     - locktime
        Time after which the timelocked script is valid to be spent

    This is a model that can be used to create smart contracts by specifying
    non-standard lifetime and timelocked scripts

    Attributes:
        _lifetime (RedeemScript): script that will allow to redeem the utxo
                                  at any time
        _timelocked (RedeemScript): script that will allwo to redeem the utxo
                                  after the specified dtime
        _locktime (): time after which the timelocked script becomes valid
        Time is specified as BIP-65:
        https://github.com/bitcoin/bips/blob/master/bip-0065.mediawiki
    """
    __slots__ = ["_lifetime_script", "_timelocked_script", "_locktime"]

    def __init__(self, lifetime, timelocked, locktime):
        """
        Initializes the time locked script with the lifetime script, timelocked
        script and locktime
        """
        self._lifetime_script = lifetime
        self._timelocked_script = timelocked
        self._locktime = locktime

    def _build(self):
        """
        Builds the script data to be able to serialize it

        The model of the timelocked script is:
            (pending)
        """
        pass

    @property
    def lifetime_script(self):
        return self._lifetime_script

    @property
    def timelocked_script(self):
        return self._timelocked_script

    @property
    def locktime(self):
        return self._locktime
