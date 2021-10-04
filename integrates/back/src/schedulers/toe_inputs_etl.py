from aioextensions import (
    collect,
    in_process,
)
import csv
from custom_exceptions import (
    GroupNameNotFound,
    InvalidField,
)
from custom_types import (
    Group,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.roots.types import (
    RootItem,
)
from db_model.toe_inputs.types import (
    ToeInput,
)
import glob
from newutils import (
    bugsnag as bugsnag_utils,
    datetime as datetime_utils,
    git as git_utils,
)
from newutils.validations import (
    validate_email_address,
)
import re
from roots import (
    domain as roots_domain,
)
import tempfile
from toe.inputs import (
    domain as toe_inputs_domain,
)
from typing import (
    Any,
    Callable,
    List,
    Set,
    Tuple,
)

bugsnag_utils.start_scheduler_session()


def _format_date(date_str: str) -> str:
    date = datetime_utils.get_from_str(date_str, date_format="%Y-%m-%d")
    formatted_date_str = date.isoformat()

    return formatted_date_str


def _format_email(email: str) -> str:
    try:
        validate_email_address(email)
        formatted_email = email
    except InvalidField:
        formatted_email = ""

    return formatted_email


def _get_group_toe_inputs_from_cvs(
    inputs_csv_path: str, group: Group, group_roots: Tuple[RootItem, ...]
) -> Set[ToeInput]:
    default_date = datetime_utils.DEFAULT_ISO_STR
    inputs_csv_fields: List[Tuple[str, Callable, Any]] = [
        # field_name, field_formater, field_default_value
        ("commit", str, ""),
        ("component", str, ""),
        ("created_date", _format_date, default_date),
        ("entry_point", str, ""),
        ("seen_first_time_by", _format_email, ""),
        ("tested_date", _format_date, default_date),
        ("verified", str, ""),
        ("vulns", str, ""),
    ]
    group_toe_inputs = set()
    with open(inputs_csv_path) as csv_file:
        for row in csv.DictReader(csv_file):
            new_toe_input = dict()
            for (field_name, formater, default_value) in inputs_csv_fields:
                cvs_field_value = row.get(field_name)
                try:
                    new_toe_input[field_name] = (
                        formater(cvs_field_value)
                        if cvs_field_value
                        else default_value
                    )
                except ValueError:
                    new_toe_input[field_name] = default_value

            new_toe_input[
                "unreliable_root_id"
            ] = roots_domain.get_unreliable_root_id_by_component(
                new_toe_input["component"], group_roots, group
            )
            new_toe_input["group_name"] = group["name"]
            group_toe_inputs.add(ToeInput(**new_toe_input))

    return group_toe_inputs


def _get_toe_inputs_to_add(
    group_toe_inputs: Set[ToeInput],
    group_toe_input_hashes: Set[int],
    cvs_group_toe_inputs: Set[ToeInput],
) -> Set[ToeInput]:
    return {
        toe_input
        for toe_input in cvs_group_toe_inputs
        if toe_input not in group_toe_inputs
        and toe_input.get_hash() not in group_toe_input_hashes
    }


def _get_toe_inputs_to_update(
    group_toe_inputs: Set[ToeInput],
    group_toe_input_hashes: Set[int],
    cvs_group_toe_inputs: Set[ToeInput],
) -> Set[ToeInput]:
    return {
        toe_input
        for toe_input in cvs_group_toe_inputs
        if toe_input not in group_toe_inputs
        and toe_input.get_hash() in group_toe_input_hashes
    }


def _get_toe_inputs_to_remove(
    group_toe_inputs: Set[ToeInput],
    cvs_group_toe_input_hashes: Set[int],
) -> Set[ToeInput]:
    return {
        toe_input
        for toe_input in group_toe_inputs
        if toe_input.get_hash() not in cvs_group_toe_input_hashes
    }


async def update_toe_inputs_from_csv(
    loaders: Dataloaders, group_name: str, inputs_csv_path: str
) -> None:
    group_roots: Tuple[RootItem, ...] = await loaders.group_roots.load(
        group_name
    )
    group_toe_inputs: Set[ToeInput] = set(
        await loaders.group_toe_inputs.load(group_name)
    )
    group: Group = await loaders.group.load(group_name)
    group_toe_input_hashes = {
        toe_input.get_hash() for toe_input in group_toe_inputs
    }
    cvs_group_toe_inputs = await in_process(
        _get_group_toe_inputs_from_cvs, inputs_csv_path, group, group_roots
    )
    cvs_group_toe_input_hashes = {
        toe_input.get_hash() for toe_input in cvs_group_toe_inputs
    }
    toe_inputs_to_update = await in_process(
        _get_toe_inputs_to_update,
        group_toe_inputs,
        group_toe_input_hashes,
        cvs_group_toe_inputs,
    )
    await collect(
        [
            toe_inputs_domain.update(toe_input)
            for toe_input in toe_inputs_to_update
        ]
    )
    toe_inputs_to_remove = await in_process(
        _get_toe_inputs_to_remove, group_toe_inputs, cvs_group_toe_input_hashes
    )
    await collect(
        [
            toe_inputs_domain.remove(
                toe_input.entry_point,
                toe_input.component,
                toe_input.group_name,
            )
            for toe_input in toe_inputs_to_remove
        ]
    )
    toe_inputs_to_add = await in_process(
        _get_toe_inputs_to_add,
        group_toe_inputs,
        group_toe_input_hashes,
        cvs_group_toe_inputs,
    )
    await collect(
        [toe_inputs_domain.add(toe_input) for toe_input in toe_inputs_to_add]
    )


def _get_group_name(tmpdirname: str, inputs_csv_path: str) -> str:
    group_match = re.match(
        pattern=fr"{tmpdirname}/groups/(\w+)", string=inputs_csv_path
    )
    if not group_match:
        raise GroupNameNotFound()

    return group_match.groups("1")[0]


async def main() -> None:
    """Update the root toe inputs from services repository"""
    loaders = get_new_context()
    with tempfile.TemporaryDirectory() as tmpdirname:
        git_utils.clone_services_repository(tmpdirname)
        inputs_csv_glob = f"{tmpdirname}/groups/*/toe/inputs.csv"
        inputs_cvs_paths = glob.glob(inputs_csv_glob)
        inputs_csv_group_names = [
            _get_group_name(tmpdirname, inputs_cvs_path)
            for inputs_cvs_path in inputs_cvs_paths
        ]
        await collect(
            [
                update_toe_inputs_from_csv(
                    loaders, group_name, inputs_csv_path
                )
                for inputs_csv_path, group_name in zip(
                    inputs_cvs_paths, inputs_csv_group_names
                )
            ]
        )
