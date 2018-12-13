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

def drive_url_filter(drive):
    """ Gets ID of the drive image """
    if(drive.find("s3.amazonaws.com") != -1):
        new_url = drive.split("/")[5]
        return new_url
    else:
        if(drive.find("id=") != -1):
            new_url = drive.split("id=")[1]
            if(new_url.find("&") != -1):
                return new_url.split("&")[0]
    return drive

def remove_standard_keys(dictionary):
    return {dictionary['field']:dictionary['value']}

def merge_dicts_list_into_dict(dicts_list):
    dicts_without_standard_keys = [remove_standard_keys(x) \
                                       for x in dicts_list]
    return reduce(dict_concatenation, dicts_without_standard_keys)

def create_dict(remission_submission):
    remission_dict = merge_dicts_list_into_dict(remission_submission["data"])
    return remission_dict

def get_finding_type(cssv2_dict):
    if 'findingType' not in cssv2_dict or cssv2_dict['findingType'] == 'Seguridad':
        finding_type = 'Vulnerabilidad'
    else:
        finding_type = cssv2_dict['findingType']
    return finding_type

def get_impact(criticity):
    criticity = float(criticity)
    impact = "Alto"
    if(criticity <= 3.9):
        impact = "Bajo"
    elif(criticity <= 6.9):
        impact = "Medio"
    else:
        impact = "Alto"
    return impact

def get_cwe_url (cwe):
    try:
        value = int(cwe)
        urlbase = 'https://cwe.mitre.org/data/definitions/:id.html'
        return urlbase.replace(':id', str(value))
    except ValueError:
        return 'None'

def is_exploitable(explotability):
    if explotability == 1.0 or explotability == 0.95:
        is_exploitable = 'Si'
    else:
        is_exploitable = 'No'
    return is_exploitable

def to_formstack(data):
    new_data = dict()
    for key, value in data.items():
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
