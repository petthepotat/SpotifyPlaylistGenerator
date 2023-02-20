VALID_CHARACTER = set(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.()[]{}!@#$%^&~`' "
)


def remove_illegal_file_chars(filename):
    """Remove illegal characters from a filename"""
    # remove emojis as well
    return "".join(c for c in filename if c in VALID_CHARACTER).strip()
