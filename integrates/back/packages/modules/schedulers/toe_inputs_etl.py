# Standard libraries
import csv
from typing import (
    Any,
    Callable,
    List,
    Set,
    Tuple,
)

# Local libraries
from data_containers.toe_inputs import GitRootToeInput
from newutils import (
    bugsnag as bugsnag_utils,
    datetime as datetime_utils,
)


bugsnag_utils.start_scheduler_session()


def _format_date(date_str: str) -> str:
    date = datetime_utils.get_from_str(date_str, date_format='%Y-%m-%d')
    formated_date_str = date.isoformat()

    return formated_date_str


def _get_group_toe_inputs_from_cvs(
    inputs_csv_path: str,
    group_name: str
) -> Set[GitRootToeInput]:
    default_date = datetime_utils.DEFAULT_ISO_STR
    inputs_csv_fields: List[Tuple[str, Callable, Any]] = [
        # field_name, field_formater, field_default_value
        ('commit', str, ''),
        ('component', str, ''),
        ('created_date', _format_date, default_date),
        ('entry_point', str, ''),
        ('seen_first_time_by', str, ''),
        ('tested_date', _format_date, default_date),
        ('verified', str, ''),
        ('vulns', str, ''),
    ]
    group_toe_inputs = set()
    with open(inputs_csv_path) as csv_file:
        for row in csv.DictReader(csv_file):
            new_toe_input = dict()
            for (
                field_name,
                formater,
                default_value
            ) in inputs_csv_fields:
                cvs_field_value = row.get(field_name)
                try:
                    new_toe_input[field_name] = (
                        formater(cvs_field_value)
                        if cvs_field_value
                        else default_value
                    )
                except ValueError:
                    new_toe_input[field_name] = default_value

            new_toe_input['group_name'] = group_name
            group_toe_inputs.add(GitRootToeInput(**new_toe_input))

    return group_toe_inputs


def _get_toe_inputs_to_add(
    group_toe_inputs: Set[GitRootToeInput],
    group_toe_input_hashes: Set[int],
    cvs_group_toe_inputs: Set[GitRootToeInput]
) -> Set[GitRootToeInput]:
    return {
        toe_input
        for toe_input in cvs_group_toe_inputs
        if toe_input not in group_toe_inputs
        and toe_input.get_hash() not in group_toe_input_hashes
    }


def _get_toe_inputs_to_update(
    group_toe_inputs: Set[GitRootToeInput],
    group_toe_input_hashes: Set[int],
    cvs_group_toe_inputs: Set[GitRootToeInput]
) -> Set[GitRootToeInput]:
    return {
        toe_input
        for toe_input in cvs_group_toe_inputs
        if toe_input not in group_toe_inputs
        and toe_input.get_hash() in group_toe_input_hashes
    }


def _get_toe_inputs_to_remove(
    group_toe_inputs: Set[GitRootToeInput],
    cvs_group_toe_input_hashes: Set[int]
) -> Set[GitRootToeInput]:
    return {
        toe_input
        for toe_input in group_toe_inputs
        if toe_input.get_hash() not in cvs_group_toe_input_hashes
    }
