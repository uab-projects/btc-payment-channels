import sys

from ....bitcoin import WIFAddress

from .create import opening
from .commit import commitment
from .consume import consume


def decodeKeys(keys_list):
    keys_decoded = []
    for key in keys_list:
        keys_decoded.append(WIFAddress.decode(key))

    return keys_decoded


if __name__ == "__main__":
    # Read args
    sel = int(sys.argv[1])

    keys = sys.argv[2:]
    keys_decoded = decodeKeys(keys)

    hash_val = "test"

    tx, redeem_multi = opening(keys_decoded)

    print("Opening transaction")
    print(tx)
    print(tx.serialize().hex())

    upd_tx, redeem_tricky = commitment(keys_decoded, tx.id, redeem_multi,
                                       selection=1)
    print("---------------------------------------------")
    print("Commitment transaction, Alice creates this one")
    print(upd_tx)
    print(upd_tx.serialize().hex())

    print("---------------------------------------------")
    print("Spend funds")

    consume_tx = consume(keys_decoded, upd_tx.id, redeem_tricky,
                         hash_val=hash_val, selection=sel)
    print(consume_tx)
    print(consume_tx.serialize().hex())
