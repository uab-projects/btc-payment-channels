# Libraries
# # App
from ...field import Opcode, OP_0, OP_1
from .model import PayScript
from .multisig import MultiSig


class TimeLockedScript(PayScript):
    """
    Defines a pay script to pay to a TimeLockedScript redeem script, providing
    methods to pay a timelocked script or unlocked script.

    Attributes:
        _selection (Serializable): selects whether we are spending the script
        in a normal condition or in a time-locked condition
        _script (Script): script that pays the TimeLockedScript redeem script
    """
    __slots__ = ["_selection", "_script"]

    def __init__(self, redeem, script=None, selection=None):
        """
        Initializes a TimeLockedScript payment script, selecting by default
        the normal condition (not time-locked) and optionally setting also
        the data to spend the script, if any

        Args:
            redeem (RedeemScript): the redeem script
            selection (mix): Opcode or int to select whether to spend the
            script in expired conditions or not. If not specified, we'll
            spend the script on the default, no-time-locked condition.
            script (Script): script with data to provide to spend the
            redeem script in the case you selected. If none, no data will
            be set
        """
        super().__init__(redeem)
        # Save
        self.selection = selection
        self._script = script

    def _build(self):
        """
        Builds the PayScript from the script and selection
        """
        self._data = [self._script, self._selection]

    @property
    def script(self):
        return self._script

    @script.setter
    def script(self, script):
        self._script = script

    @property
    def selection(self):
        return self._selection

    @property
    def multisig(self):
        """ Returns a MultiSig PayScript if it's needed to be used """
        return MultiSig(self._redeem)

    @selection.setter
    def selection(self, selection):
        assert isinstance(selection, int) or \
               isinstance(selection, Opcode) or selection is None, \
               "The selection must be either an integer, opcode or None" \
               + " to select the default, no-time-locked script"
        # Convert and check selection
        if isinstance(selection, Opcode):
            # OPCODE used
            assert isinstance(selection, OP_1) or \
             isinstance(selection, OP_0), "The OPCODE has to be 0 or 1"
        elif isinstance(selection, int):
            # Int or boolean used
            selection = int(selection)  # For booleans
            assert selection == 0 or selection == 1, "The selection " + \
                "must be 0 or 1"
            selection = OP_0 if selection == 0 else OP_1
        else:
            # Default
            selection = OP_1
        self._selection = selection

    @property
    def spend_before_locktime(self):
        """
        Returns True if the selection set is to spend the redeem script before
        the locktime arrives (or at anytime depending on how it's coded)
        """
        return self._selection == OP_0

    @spend_before_locktime.setter
    def spend_before_locktime(self, value):
        """
        Allows to set the spend_before_locktime property by changing the
        selection
        """
        self.selection = not value

    @property
    def spend_after_locktime(self):
        """
        Returns true if the selection set is to spend the redeem script after
        the lock time, using the timelocked_script.
        """
        return self._selection == OP_1

    @spend_after_locktime.setter
    def spend_after_locktime(self, value):
        """
        Allows to set the spend_after_locktime property by changing the
        selection
        """
        self.selection = value
