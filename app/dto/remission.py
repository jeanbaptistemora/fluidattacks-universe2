""" DTO to map remission submission to Integrates format """
# Disabling this rule is necessary for importing modules beyond the top level
# pylint: disable=relative-beyond-top-level

from datetime import datetime
from ..utils import forms

# Remission form url
URL = "https://www.formstack.com/api/v2/form/1892477/submission.json"
PROJECT_FIELD_ID = "29187648"


def parse(submission, initial_dict):
    try:
        remission_fields = {
            "29187648": "FLUID_PROJECT",
            "29187692": "SERVICE",
            "29187890": "LEADER",
            "35631688": "LAST_REMISSION"
        }
        parsed_dict = {remission_fields[k]: initial_dict[k]
                       for (k, v) in list(remission_fields.items())}
        parsed_dict["TIMESTAMP"] = submission["timestamp"]
        parsed_dict["APPROVAL_STATUS"] = submission["approval_status"]
        return parsed_dict
    except KeyError:
        project_field = {
            "29187648": "FLUID_PROJECT",
        }
        parsed_dict = {project_field[k]: initial_dict[k]
                       for (k, v) in list(project_field.items())}
        return parsed_dict


def create_dict(remission_submission):
    remission_dict = forms.merge_dicts_list_into_dict(remission_submission["data"])
    return parse(remission_submission, remission_dict)


def get_lastest(remissions_list):
    return max(remissions_list, key=lambda x: x['TIMESTAMP'])


def days_until_now(date):
    delta_until_now = datetime.now() - forms.string_to_date(date)
    return forms.round_date(delta_until_now)
