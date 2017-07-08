"""
Helper methods to ease the tasks of dealing with bytes in Python and with
Bitcoin fields as bytes in general
"""
# Constants
HEX_STR_PRE = "0x"
"""
    str: Prefix to denote an hex string
"""
HEX_STR_LEN_MAX = 200
"""
    int: Defines the maximum length of an hexa string to be converted
"""


def bfh(hexa):
    """
    Little helper that converts a string of hex-digits into a bytes object

    Args:
        hexa (str): string of hex digits
    Returns:
        bytes: byte object with the contents of the hex string
    """
    return bytes().fromhex(hexa)


def value_to_hex(value):
    """
    Converts a value into a string, trying to set it as an hex string if found
    a bytes object or a number

    Just converts to hex string bytes and bytearray objects, and positive or
    zero integers. The rest of values will return str(value)

    Args:
        value (mixed): value to convert to hex string
    Returns:
        str: hexa string or str(value) if no conversible value found
    """
    value_as_str = str(value)
    # Convert
    if isinstance(value, bytes) or isinstance(value, bytearray):
        value_as_str = HEX_STR_PRE+value.hex()
    elif isinstance(value, int):
        if value >= 0:
            value_as_str = (HEX_STR_PRE+"{0:02x}").format(value)
    # Reduce
    if value_as_str.startswith(HEX_STR_PRE) and \
       len(value_as_str) > HEX_STR_LEN_MAX:
        value_as_str = value_as_str[:HEX_STR_LEN_MAX]+"..."
    return value_as_str
