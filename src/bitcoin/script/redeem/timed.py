"""
Defines RedeemScripts that contain time conditions in order to spend funds
"""
# Libraries
# # App
from .model import RedeemScript
from ...field.opcode import OP_IF, OP_ELSE, OP_ENDIF, OP_CHECKLOCKTIMEVERIFY, \
                            OP_DROP


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
                                  after the specified time
        _lifetime_params (Serializable): parameters to add to the lifetime
            script so it is spendable before the time specified
        _timelocked_params (Serializable): parameters to add to the timelocked
            script so it is spendable after the given time
        _locktime (VarInt):
            time after which the timelocked script becomes valid
        Time is specified as BIP-65:
        https://github.com/bitcoin/bips/blob/master/bip-0065.mediawiki
    """
    __slots__ = ["_lifetime_script", "_timelocked_script", "_locktime"]

    def __init__(self, lifetime, timelocked, locktime, lifetime_params=None,
                 timelocked_params=None):
        """
        Initializes the time locked script with the lifetime script, timelocked
        script and locktime
        """
        self._lifetime_script = lifetime
        self._timelocked_script = timelocked
        self._locktime = locktime
        self._lifetime_params = lifetime_params
        self._timelocked_params = timelocked_params

    def _build(self):
        """
        Builds the script data to be able to serialize it

        The model of the timelocked script is:
            OP_IF
                <time> OP_CHECKLOCKTIMEVERIFY OP_DROP
                <timelocked_script>
                <timelocked_params>
            OP_ELSE
                <lifetime_params>
            OP_ENDIF
            <lifetime_script>
        """
        # Switch if / else to spend after / before the time lock gets
        self._data = [OP_IF]
        # CASE TO SPEND AFTER LOCKED TIME:
        self._data += [self._locktime, OP_CHECKLOCKTIMEVERIFY, OP_DROP]
        self._data += [self._timelocked_script]
        if self._timelocked_params is not None:
            self._data += [self._timelocked_params]
        # CASE TO SPEND BEFORE LOCKED TIME:
        if self._lifetime_params is not None:
            self._data += [OP_ELSE, self._lifetime_params]
        # End of conditions
        self._data += [OP_ENDIF]
        # Lifetime script
        self._data.append(self._lifetime_script)

    @property
    def lifetime_script(self):
        return self._lifetime_script

    @property
    def timelocked_script(self):
        return self._timelocked_script

    @property
    def locktime(self):
        return self._locktime
