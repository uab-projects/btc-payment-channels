"""
Defines several data structures used in low-level bitcoin for carrying data
in the protocol as fields in transactions, blocks...

Classes defined here are only used inside the app to provide easy storage and
serialization, it's not inteded to use for the app user. This way, this classes
provided here should only be used to create data structure that will deal with
Python data types and may use this classes just to store them, knowing that
they will also provide serialization methods.

The following classes allow to deal with low-level data providing methods to
easily handle the data in fields and providing methods to transform them into
an array of bytes compatible with the Bitcoin standards definition and
vice-versa

For convention purposes, we'll use special notation when naming classes.
These prefixes may be applied:

 - Size prefix:
   Some fields have a fixed size. In this case, a prefix is added with the
   following components:
    - If the field has sign or not
      U for unsigned, S for signed
    - Field size in bytes
      The size followed by a B indicating it's the size in bytes
   Example: U4B specifies an unsigned 4 byte field
   If the field has no fixed size, then prefix Var is used

 - Endianness prefix:
   The prefix LE will be understood as little endian and BE for big endian.
   If nothing specified, big endian is used.

When naming classes, also a special convention will be used to specify the
data type it's containing:
 - Int: any number field, either positive or negative and size-independent
 - Str: any string field

Classes are added as needed so maybe many possible fields may exist in the
Bitcoin protocol but not available here because it's not used anywhere.
"""
