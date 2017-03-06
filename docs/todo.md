## TO-DO
### General level
 - [ ] `src.address.address`
     - [ ] Address class to generate an adress from base58 string and bytes object
 - [ ] `src.address.prefix`
     - [ ] Prefixes of addresses using base58
     - [ ] Different networks prefixes
### Transaction level
#### Inputs and outputs
 - [ ] `src.bitcoin.tx` -> `src.bitcoin.tx.tx`
 - [ ] `src.bitcoin.tx.__init__`
     - [ ] `From .tx import Tx`
     - [ ] `__all__ = ["Tx"]`
 - [ ] `src.bitcoin.tx.input`
     - [ ] Attributes `utxoId, utxoNum, script, sequence`
     - [ ] Default `sequence` & search other fields types
     - [ ] Serialization of the input
     - [ ] Deserialization of the input
 - [ ] `src.bitcoin.tx.output`
     - [ ] Attributes `value, script`
     - [ ] Search fields types
     - [ ] Serialization of the output
     - [ ] Deserialization of the output
#### Scripting
 - [ ] `src.bitcoin.script.general`
     - [ ] General class `Script`
     - [ ] Attributes `_data`
     - [ ] Property `data`
     - [ ] Implements serialization
     - [ ] Implements deserialization
 - [ ] `src.bitcoin.script.sig`
     - [ ] General class `ScriptSig`, inherits from `Script`, no extra attrs.
     - [ ] Specific class `P2PKH`, inherits from `ScriptSig`
         - [ ] Constructor attaches script to the input
         - [ ] Saves input where the script will be attached
         - [ ] Input passed to constructor
         - [ ] Constructor builds the script P2PKH into its `_data`
         - [ ] Method `sign`, undefined
     - [ ] Specific class `P2SH`, inherits from `ScriptSig`
         - [ ] Constructor requires the script to pay to
 - [ ] `src.bitcoin.script.sig`
     - [ ] General class `ScriptPubKey`, inherits from `Script`, extra `Address` attribute
         - [ ] Constructor initializes attribute address
         - [ ] Facilitator method that given an address creates the proper `ScriptPubKey`
     - [ ] Specific class `P2PKH`, inherits from `ScriptPubKey`
         - [ ] In the constructor, calls super
         - [ ] Initializes the script contents with `P2PKH` script
     - [ ] Specific class `P2SH`, inherits from `ScriptPubKey`
         - [ ] In the constructor, calls super
         - [ ] Initializes the script contents with `P2SH` script
