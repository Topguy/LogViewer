
import re

def filter_lines(lines, include_text=None, exclude_text=None, include_regex=None, exclude_regex=None, case_sensitive=True):
    """
    Filters a list of text lines based on include/exclude criteria for both plain text and regex.

    Args:
        lines (list): A list of strings, where each string is a line of text.
        include_text (str, optional): Text that must be present in a line for it to be included.
        exclude_text (str, optional): Text that must not be present in a line for it to be included.
        include_regex (str, optional): A regex pattern that a line must match to be included.
        exclude_regex (str, optional): A regex pattern that a line must not match to be included.
        case_sensitive (bool, optional): If False, all text comparisons will be case-insensitive. Defaults to True.

    Returns:
        list: A new list of strings containing the filtered lines.
    """
    filtered = lines

    flags = 0 if case_sensitive else re.IGNORECASE

    # Include text filter
    if include_text:
        if case_sensitive:
            filtered = [line for line in filtered if include_text in line]
        else:
            filtered = [line for line in filtered if include_text.lower() in line.lower()]

    # Exclude text filter
    if exclude_text:
        if case_sensitive:
            filtered = [line for line in filtered if exclude_text not in line]
        else:
            filtered = [line for line in filtered if exclude_text.lower() not in line.lower()]

    # Include regex filter
    if include_regex:
        try:
            pattern = re.compile(include_regex, flags)
            filtered = [line for line in filtered if pattern.search(line)]
        except re.error as e:
            # Handle invalid regex gracefully, maybe log the error or return an empty list
            print(f"Invalid include regex: {e}")
            return []

    # Exclude regex filter
    if exclude_regex:
        try:
            pattern = re.compile(exclude_regex, flags)
            filtered = [line for line in filtered if not pattern.search(line)]
        except re.error as e:
            print(f"Invalid exclude regex: {e}")
            return []

    return filtered
