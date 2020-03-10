# coding=utf-8
""" Auxiliar functions for forms handling """

from datetime import datetime
from typing import Dict, List

# pylint: disable=redefined-builtin
try:
    type(reduce)
except NameError:
    from functools import reduce


def dict_concatenation(
        dict_1: Dict[object, object], dict_2: Dict[object, object]) -> Dict[object, object]:
    dict_1_copy = dict_1.copy()
    dict_1_copy.update(dict_2)
    return dict_1_copy


def remove_standard_keys(dictionary: Dict[object, object]) -> Dict[object, object]:
    return {dictionary['field']: dictionary['value']}


def merge_dicts_list_into_dict(dicts_list: List[Dict[object, object]]) -> Dict[object, object]:
    dicts_without_standard_keys = [remove_standard_keys(x)
                                   for x in dicts_list]
    return reduce(dict_concatenation, dicts_without_standard_keys)


def is_exploitable(explotability: float, version: str) -> str:
    if version == '3.1':
        if explotability >= 0.97:
            exploitable = 'Si'
        else:
            exploitable = 'No'
    else:
        if explotability in (1.0, 0.95):
            exploitable = 'Si'
        else:
            exploitable = 'No'
    return exploitable


def string_to_date(string: str) -> datetime:
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
