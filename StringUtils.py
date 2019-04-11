"""
Utility functions for string manipulation.
@author Sergey Goldobin
4/11/19
"""


def is_substring_at(source, i, target):
    """
    Is a given target a substring of source at index i?
    :param source: (str) The source string
    :param i: (int) The index to check at.
    :param target: (str) The target substring
    :return:
    """
    return source[i:i+(len(target))] == target


def string_skip(string, start_index, target, nested_by=''):
    """
    Starting from a given string index, scroll until a matching closing subgroup is found.
    :param string: (str) -- String to scroll through
    :param start_index: (int) -- Index in the string to start with.
    :param target: (str) -- A group of closing characters to match.
    :param nested_by: (str) -- A subgroup that constitutes nesting.
    :return: (int) The index of the first character after the target.
    """
    i = start_index
    nesting_level = 0

    while i < len(string):
        # found a nesting block
        if nested_by != '' and is_substring_at(string, i, nested_by):
            nesting_level += 1

        # Found a closing block
        if is_substring_at(string, i, target):
            if nesting_level == 0:  # Found the proper closing block
                return i + len(target)
            else:  # De-nest
                nesting_level -= 1

        # If no match, just continue
        i += 1
