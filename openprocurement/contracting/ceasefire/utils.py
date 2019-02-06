# -*- coding: utf-8 -*-
def view_milestones_by_type(milestones, type_key='type_'):
    """Returns dict of milestones, where key is the type of milestone

    Use this tool to not fetch milestone only by it's index.
    """
    result = {}
    for milestone in milestones:
        result[milestone[type_key]] = milestone

    return result
