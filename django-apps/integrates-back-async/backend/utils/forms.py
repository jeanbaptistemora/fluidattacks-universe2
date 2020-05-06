# coding=utf-8
""" Auxiliar functions for forms handling """

from typing import Dict


def dict_concatenation(
        dict_1: Dict[object, object], dict_2: Dict[object, object]) -> Dict[object, object]:
    dict_1_copy = dict_1.copy()
    dict_1_copy.update(dict_2)
    return dict_1_copy


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
