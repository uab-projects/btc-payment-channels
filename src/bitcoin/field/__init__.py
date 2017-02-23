"""
Defines several data structures used in low-level bitcoin for carrying data
in the protocol as fields in transactions, blocks...

Modules defined here are only used inside the app to provide easy storage and
serialization, it's not inteded to use for the app user. This way, this classes
provided here should only be used to create data structure that will deal with
Python data types and may use this classes just to store them, knowing that
they will also provide serialization methods.

The following modules allow to deal with low-level data providing methods to
easily handle the data in fields and providing methods to transform them into
an array of bytes compatible with the Bitcoin standards definition and
vice-versa

Modules and classesare added as needed so maybe many possible fields may exist
in the Bitcoin protocol but not available here because it's not used anywhere.
"""
