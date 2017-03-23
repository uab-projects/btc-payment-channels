"""
Script of general purpose, containing all the data and the methos needed to
create a general script. It also implements the most common scripts used in the
main network and provides an interface to create the scriptsig and the
scriptpubkey that will allow the user to create transactions and later, spend
the UTXO created.
"""
# Libraries
from ..interfaces import Serializable


class Script(Serializable):
    """
    Main scripting class of the application
    """
    __slots__ = ["_data"]

    def __init__(self):
        self._data = []

    def serialize(self):
        """
        Serializes the contents of the current class into an array of bytes so
        the class can be represented as an array of bytes compatible with what
        the Bitcoin protocol specifies

        Returns:
            bytes: data of the class serialized in a bytes object
        """
        serialized = [x.serialize() for x in self._data]
        return b''.join(serialized)

    @classmethod
    def deserialize(cls, data):
        """
        Deserializes the contents of the data passed to try make them fit into
        the class model. If the data has invalid length or invalid data,
        appropiate exceptions will be raised.

        Please implement this method in a way that can receive more data than
        the strictly required in variable sized fields, so it will help caller
        methods to detect size after calling deserialization

        Args:
            data (bytes): a bytes object containing data to de-serialize

        Returns:
            the instance of the class filled with the data if succeeded

        Raises:
            ValueError: if data can't be fit into the model
        """
        pass

    def __len__(self):
        """ Returns the size of the serialized script in bytes """
        return len(self.serialize())
