"""
Script of general purpose, containing all the data and the methos needed to
create a general script. It also implements the most common scripts used in the
main network and provides an interface to create the scriptsig and the
scriptpubkey that will allow the user to create transactions and later, spend
the UTXO created.
"""

from ..interfaces import Serializable


class Script(Serializable):
    pass
