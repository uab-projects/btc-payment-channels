"""
General purpose script, modelling all the data and the methods needed to
create a generalistic script.
"""
# Libraries
# # App
from ..interfaces import Serializable


class Script(Serializable):
    """
    Defines how every script must look like and behave.

    Every script will have some internal values to build the script. When
    the serialization is needed, the serialize method will call the method
    `_build`, that has to update a list of serializable items that contain
    opcodes and data that creates the script (attribute `_data`)

    The `_build` method has to update the data so it contains the updated
    values of the script. Please be careful to implement `_build` so that
    it can be called multiple times and the attribute `_data` stays updated

    Attributes:
        _data (list): list of serializable items of the script (opcodes
        and data)
    """
    __slots__ = ["_data"]

    def __init__(self, data=None):
        """
        Initializes a script given the data to contain

        Args:
            data (list): list of serializable items that conform the script
        """
        self._data = [] if data is None else data

    def _build(self):
        """
        Updates the `_data` attribute before serializing and printing
        (maybe some attributes have changed and the script needs to be updated)

        If not implemented, does nothing
        """
        pass

    def serialize(self):
        """
        Serializes the contents of the current class into an array of bytes so
        the class can be represented as an array of bytes compatible with what
        the Bitcoin protocol specifies.

        First, calls method `_build` to update the `_data` attribute if
        necessary

        Returns:
            bytes: data of the script serialized in a bytes object
        """
        # Update data
        self._build()
        # Serialize data
        return b''.join([x.serialize() for x in self._data])

    @classmethod
    def deserialize(cls, data):
        """
        Deserializes the bytes data object as a script
        """
        raise NotImplementedError("Script deserialization has not been " +
                                  "implemented yet")

    def __str__(self, space=""):
        """
        Prints the script by printing each field in the data
        """
        # Update script contents
        self._build()
        # Create string
        txt = ""
        txt += "%s" % space
        for field in self._data:
            txt += "%s " % (str(field))
        return txt


class TxInputOutputScript(Script):
    """
    Script that belongs to a transaction input / output (model for
    scriptPubKey and scriptSig)

    Attributes:
        _parent (TxInputOutput): parent transaction i/o it belongs to
    """
    __slots__ = ["_parent"]

    def __init__(self, parent=None, data=None):
        """
        Initializes an i/o script given the parent and data
        """
        super().__init__(data)
        self._parent = parent

    @property
    def parent(self):
        """
        Returns the transaction input / output the script belongs to, if any
        """
        return self._parent

    @parent.setter
    def parent(self, new_parent):
        """
        Sets the script of the input / output

        Args:
            new_parent (TxInputOutput): the input / output it belongs to
                             can be None to set no no input output related
                             will also set the script of the input / output of
                             the script as itself
        """
        # Remove script assignment
        old_parent = self._parent
        self._parent = new_parent
        # Remove itself from previous transaction i/o
        if old_parent is not None \
           and old_parent.script == self:
            old_parent.script = None
        # Add itself to new script
        if new_parent is not None \
           and new_parent.script != self:
            new_parent.script = self
