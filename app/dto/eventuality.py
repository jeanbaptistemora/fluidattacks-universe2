":"""" DTO to map the Integrates fields to formstack """

def create(parameter):
    """ Converts the index of a JSON to Formstack index """
    events_dict={}
    status_field_id = "29062640"
    events_fields = {
        "29042322":"fluidProject",
        "29042542":"affectation"
    }
    parsed_dict = {k:parameter["vuln[" + v + "]"] \
            for (k,v) in events_fields.items()}
    if parameter["vuln[affectation]"] != "":
        parsed_dict[status_field_id] = "Tratada"
    else:
        parsed_dict[status_field_id] = parameter["vuln[status]"]
    events_dict["request_id"] = parameter["vuln[id]"]
    events_dict["data"] = to_formstack(parsed_dict)
    return events_dict

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

def parse(submission_id, request_arr):
    initial_dict = create_dict(request_arr)
    events_fields = {
        "29042426":"analyst",
        "29042288":"client",
        "29042322":"fluidProject",
        "39595967":"clientProject",
        "29042327":"type",
        "29042402":"detalle",
        "29042174":"fecha",
        "29062640":"estado",
        "29042542":"affectation",
        "29042411":"evidence",
        "57917686":"accessibility",
        "52661157":"affectedComponents"
    }
    parsed_dict = {events_fields[k]:initial_dict[k] \
                   if k in initial_dict.keys() else "" \
                   for (k,v) in events_fields.items()}
    parsed_dict["id"] = submission_id
    return parsed_dict


def to_formstack(data):
    new_data = dict()
    for key, value in data.iteritems():
        new_data["field_"+ str(key)] = value
    return new_data
