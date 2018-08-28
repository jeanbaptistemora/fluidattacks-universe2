""" DTO to map remission submission to Integrates format """

from datetime import datetime

# Remission form url
URL = "https://www.formstack.com/api/v2/form/1892477/submission.json"
PROJECT_FIELD_ID = "29187648"

def parse(submission, initial_dict):
    remission_fields = {
        "29187648":"FLUID_PROJECT",
        "29187692":"SERVICE",
        "29187890":"LEADER",
        "35631688":"LAST_REMISION"
    }
    parsed_dict = {remission_fields[k]:initial_dict[k] \
            for (k,v) in remission_fields.items()}
    parsed_dict["timestamp"] = submission["timestamp"]
    return parsed_dict

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
    return parse(remission_submission, remission_dict)

def get_lastest(remissions_list):
    return max(remissions_list, key=lambda x:x['timestamp'])

def string_to_date(string):
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

def round_date(date):
    seconds_in_hour = 3600
    hours = round(date.seconds/seconds_in_hour)
    if hours > 12:
        rounded_date = date.days + 1
    else:
        rounded_date = date.days
    return rounded_date

def days_until_now(date):
    delta_until_now = datetime.now() - string_to_date(date)
    return round_date(delta_until_now)
