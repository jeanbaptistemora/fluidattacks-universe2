""" DTO to map remission submission to Integrates format """

# Remission form url
RM_URL = "https://www.formstack.com/api/v2/form/1892477/submission.json"

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
