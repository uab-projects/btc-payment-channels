## TO-DO
### Testing
 - [ ] Test transaction P2PKH using our software
### General level
 - [x] `src.address.address`
     - [x] Address class to generate an adress from base58 string and bytes object
 - [x] `src.address.prefix`
     - [x] Prefixes of addresses using base58
     - [x] Different networks prefixes
### Transaction level
#### Inputs and outputs
 - [ ] `src.bitcoin.tx` -> `src.bitcoin.tx.tx`
 - [ ] `src.bitcoin.tx.__init__`
     - [ ] `From .tx import Tx`
     - [ ] `__all__ = ["Tx"]`
 - [ ] `src.bitcoin.tx.input`
     - [x] Attributes `utxoId, utxoNum, script, sequence`
     - [x] Default `sequence` & search other fields types
     - [x] Serialization of the input
     - [ ] Deserialization of the input
 - [ ] `src.bitcoin.tx.output`
     - [x] Attributes `value, script`
     - [x] Search fields types
     - [x] Serialization of the output
     - [ ] Deserialization of the output
#### Scripting
 - [ ] `src.bitcoin.script.general`
     - [x] General class `Script`
     - [x] Attributes `_data`
     - [ ] Property `data`
     - [x] Implements serialization
     - [ ] Implements deserialization
 - [ ] `src.bitcoin.script.sig`
     - [x] General class `ScriptSig`, inherits from `Script`, no extra attrs.
     - [x] Specific class `P2PKH`, inherits from `ScriptSig`
         - [x] Constructor attaches script to the input
         - [x] Saves input where the script will be attached
         - [x] Input passed to constructor
         - [x] Constructor builds the script P2PKH into its `_data`
         - [x] Method `sign`, undefined
         - [x] Method `sign`, defined
     - [ ] Specific class `P2SH`, inherits from `ScriptSig`
         - [ ] Constructor requires the script to pay to
 - [ ] `src.bitcoin.script.pubkey`
     - [ ] General class `ScriptPubKey`, inherits from `Script`, extra `Address` attribute
         - [ ] Constructor initializes attribute address
         - [ ] Facilitator method that given an address creates the proper `ScriptPubKey`
     - [ ] Specific class `P2PKH`, inherits from `ScriptPubKey`
         - [ ] In the constructor, calls super
         - [ ] Initializes the script contents with `P2PKH` script
     - [ ] Specific class `P2SH`, inherits from `ScriptPubKey`
         - [ ] In the constructor, calls super
         - [ ] Initializes the script contents with `P2SH` script
