"""
Defines RedeemScripts that contain time conditions in order to spend funds
"""
# Libraries
# # App
from .. import pay
from .model import RedeemScript
from ...field import OP_IF, OP_ELSE, OP_ENDIF, OP_CHECKLOCKTIMEVERIFY, \
                            OP_DROP, ScriptData, ScriptNum


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
        _lifetime (Script): script that will allow to redeem the utxo
                                  at any time
        _timelocked (Script): script that will allwo to redeem the utxo
                                  after the specified time
        _locktime (VarInt):
            time after which the timelocked script becomes valid
        _unlocked_script (Serializable):
        _timelocked_params (Serializable): parameters to add to the timelocked
            script so it is spendable after the given time
        Time is specified as BIP-65:
        https://github.com/bitcoin/bips/blob/master/bip-0065.mediawiki
    """
    __slots__ = ["_lifetime_script", "_timelocked_script", "_unlocked_script",
                 "_locktime"]

    def __init__(self, locktime, lifetime_script=None, unlocked_script=None,
                 timelocked_script=None):
        """
        Initializes the time locked script with the lifetime script, timelocked
        script and locktime
        """
        super().__init__(None)
        self._locktime = locktime
        self._lifetime_script = lifetime_script
        self._timelocked_script = timelocked_script
        self._unlocked_script = unlocked_script

    def _build(self):
        """
        Builds the script data to be able to serialize it

        The model of the timelocked script is:
            OP_IF
                <time> OP_CHECKLOCKTIMEVERIFY OP_DROP
                <timelocked_script>
            OP_ELSE
                <unlocked_script>
            OP_ENDIF
            <lifetime_script>

        So if you want to spend the script after the locked time, you must
        specify in the payment script a OP_1 (OP_TRUE), and OP_0 (OP_FALSe)
        if you want to spend it before (or at anytime if provided a
        lifetime_script).

        Remember to put the payment script before the OP_0, OP_1
        """
        # Switch if / else to spend after / before the time lock gets
        self._data = [OP_IF]
        # CASE TO SPEND AFTER LOCKED TIME:
        self._data += [ScriptData(ScriptNum(self._locktime)),
                       OP_CHECKLOCKTIMEVERIFY, OP_DROP]
        # # Script to spend after locked time, if any
        if self._timelocked_script is not None:
            self._data += [self._timelocked_script]
        # CASE TO SPEND BEFORE LOCKED TIME, if any
        if self._unlocked_script is not None:
            self._data += [OP_ELSE, self._unlocked_script]
        # End of conditions
        self._data += [OP_ENDIF]
        # Lifetime script, if any
        if self._lifetime_script is not None:
            self._data += [self._lifetime_script]

    @property
    def lifetime_script(self):
        return self._lifetime_script

    @property
    def timelocked_script(self):
        return self._timelocked_script

    @property
    def locktime(self):
        return self._locktime

    @property
    def pay_script(self):
        return pay.TimeLockedScript(self)
