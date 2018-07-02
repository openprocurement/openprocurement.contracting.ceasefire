# -*- coding: utf-8 -*-


def search_list_with_dicts(container, key, value):
    """Search for dict in list with dicts

    Useful for searching for milestone in the list of them.

    :param container: an iterable to search in
    :param key: key of dict to check
    :param value: value of key to search

    :returns: first acceptable dict
    """
    for item in container:
        found_value = item.get(key, False)
        if found_value and found_value == value:
            return item


def view_milestones_by_type(milestones):
    """Returns dict of milestones, where key is the type of milestone

    Use this tool to not fetch milestone only by it's index.
    """
    result = {}
    for milestone in milestones:
        result[milestone.type_] = milestone

    return result
