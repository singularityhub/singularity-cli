def decodeUtf8String(inputStr):
    """Convert an UTF8 sequence into a string

    Required for compatibility with Python 2 where str==bytes
    """
    return inputStr if isinstance(inputStr, str) or not isinstance(inputStr, bytes) else inputStr.decode('utf8')
