# coding=utf-8
""" Auxiliar functions for forms handling """

from datetime import datetime

# pylint: disable=redefined-builtin
try:
    type(reduce)
except NameError:
    from functools import reduce


def dict_concatenation(dict_1, dict_2):
    dict_1_copy = dict_1.copy()
    dict_1_copy.update(dict_2)
    return dict_1_copy


def remove_standard_keys(dictionary):
    return {dictionary['field']: dictionary['value']}


def merge_dicts_list_into_dict(dicts_list):
    dicts_without_standard_keys = [remove_standard_keys(x)
                                   for x in dicts_list]
    return reduce(dict_concatenation, dicts_without_standard_keys)


def is_exploitable(explotability, version):
    if version == '3':
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


def round_date(date):
    seconds_in_hour = 3600
    hours = round(date.seconds / seconds_in_hour)
    if hours > 12:
        rounded_date = date.days + 1
    else:
        rounded_date = date.days
    return rounded_date


def string_to_date(string):
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
