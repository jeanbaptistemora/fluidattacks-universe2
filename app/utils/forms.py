""" Auxiliar functions for forms handling """

from datetime import datetime

def dict_concatenation(dict_1, dict_2):
    dict_1_copy = dict_1.copy()
    dict_1_copy.update(dict_2)
    return dict_1_copy

def remove_standard_keys(dictionary):
    return {dictionary['field']:dictionary['value']}

def merge_dicts_list_into_dict(dicts_list):
    dicts_without_standard_keys = [remove_standard_keys(x) \
                                       for x in dicts_list]
    return reduce(dict_concatenation, dicts_without_standard_keys)

def create_dict(remission_submission):
    remission_dict = merge_dicts_list_into_dict(remission_submission["data"])
    return remission_dict

def to_formstack(data):
    new_data = dict()
    for key, value in data.iteritems():
        new_data["field_"+ str(key)] = value
    return new_data

def round_date(date):
    seconds_in_hour = 3600
    hours = round(date.seconds/seconds_in_hour)
    if hours > 12:
        rounded_date = date.days + 1
    else:
        rounded_date = date.days
    return rounded_date

def string_to_date(string):
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
