"""
Tests the TxOutput model and factories
"""
# Libraries
from .factory import p2pkh

if __name__ == "__main__":
    # tx a0cdf43a2832e923c9ae629268405c2c7c32c36fba4465bf6e103f6ab33d8b2b
    output = bytes().fromhex("4b5ac400000000001976a9147c4338dea7964947b3f0954f"
                             "61ef40502fe8f79188ac")
    output_val = 0.12868171
    output_address = "1CL3KTtkN8KgHAeWMMWfG9CPL3o5FSMU4P"
    # create output
    output_obj = p2pkh(output_val, output_address)
    if(output_obj.serialize() == output):
        print("Test passed")
