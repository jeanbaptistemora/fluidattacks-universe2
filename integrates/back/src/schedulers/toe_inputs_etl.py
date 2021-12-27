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
from datetime import (
    datetime,
)
from db_model.roots.types import (
    GitRootItem,
    RootItem,
    URLRootItem,
)
from db_model.toe_inputs.types import (
    GroupToeInputsRequest,
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
from toe.inputs.types import (
    ToeInputAttributesToAdd,
    ToeInputAttributesToUpdate,
)
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
)

bugsnag_utils.start_scheduler_session()


def _format_date(iso_date_str: str) -> Optional[datetime]:
    try:
        formatted_date = (
            datetime_utils.as_zone(datetime.fromisoformat(iso_date_str))
            if iso_date_str
            else None
        )
    except ValueError:
        formatted_date = None
    return formatted_date


def _format_date_str(date_str: str) -> str:
    date = datetime_utils.get_from_str(date_str, date_format="%Y-%m-%d")
    formatted_date_str = datetime_utils.get_as_utc_iso_format(date)
    if formatted_date_str == datetime_utils.DEFAULT_ISO_STR:
        return ""
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
) -> Dict[int, ToeInput]:
    inputs_csv_fields: List[Tuple[str, Callable, Any]] = [
        # field_name, field_formater, field_default_value
        ("commit", str, ""),
        ("component", str, ""),
        ("created_date", _format_date_str, ""),
        ("entry_point", str, ""),
        ("seen_first_time_by", _format_email, ""),
        ("tested_date", _format_date_str, ""),
        ("verified", str, ""),
        ("vulns", str, ""),
    ]
    group_toe_inputs: Set[ToeInput] = set()
    with open(  # pylint: disable=unspecified-encoding
        inputs_csv_path
    ) as csv_file:
        for row in csv.DictReader(csv_file):
            new_toe_input = {}
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

            unreliable_root = roots_domain.get_unreliable_root_by_component(
                new_toe_input["component"], group_roots, group
            )
            be_present = (
                unreliable_root.state.status == "ACTIVE"
                if isinstance(unreliable_root, (GitRootItem, URLRootItem))
                else False
            )
            new_toe_input["unreliable_root_id"] = (
                unreliable_root.id if unreliable_root is not None else ""
            )
            new_toe_input["group_name"] = group["name"]
            new_toe_input["attacked_at"] = _format_date(
                new_toe_input["tested_date"]
            )
            new_toe_input["attacked_by"] = ""
            new_toe_input["be_present"] = be_present
            new_toe_input["be_present_until"] = (
                None if be_present else datetime_utils.get_utc_now()
            )
            new_toe_input["first_attack_at"] = _format_date(
                new_toe_input["tested_date"]
            )
            new_toe_input["seen_at"] = (
                _format_date(new_toe_input["created_date"])
                or _format_date(new_toe_input["tested_date"])
                if new_toe_input["seen_first_time_by"]
                else None
            )
            group_toe_inputs.add(
                ToeInput(
                    attacked_at=new_toe_input["attacked_at"],
                    attacked_by=new_toe_input["attacked_by"],
                    be_present=new_toe_input["be_present"],
                    be_present_until=new_toe_input["be_present_until"],
                    component=new_toe_input["component"],
                    entry_point=new_toe_input["entry_point"],
                    first_attack_at=new_toe_input["first_attack_at"],
                    group_name=new_toe_input["group_name"],
                    seen_at=new_toe_input["seen_at"],
                    seen_first_time_by=new_toe_input["seen_first_time_by"],
                    unreliable_root_id=new_toe_input["unreliable_root_id"],
                )
            )

    return {toe_input.get_hash(): toe_input for toe_input in group_toe_inputs}


async def add_toe_inputs(
    group_toe_inputs: Dict[int, ToeInput],
    cvs_group_toe_inputs: Dict[int, ToeInput],
) -> None:
    await collect(
        tuple(
            toe_inputs_domain.add(
                group_name=cvs_toe_input.group_name,
                component=cvs_toe_input.component,
                entry_point=cvs_toe_input.entry_point,
                attributes=ToeInputAttributesToAdd(
                    attacked_at=cvs_toe_input.attacked_at,
                    attacked_by=cvs_toe_input.attacked_by,
                    be_present=cvs_toe_input.be_present,
                    first_attack_at=cvs_toe_input.first_attack_at,
                    seen_at=cvs_toe_input.seen_at,
                    seen_first_time_by=cvs_toe_input.seen_first_time_by,
                    unreliable_root_id=cvs_toe_input.unreliable_root_id,
                ),
            )
            for cvs_toe_input in cvs_group_toe_inputs.values()
            if cvs_toe_input.get_hash() not in group_toe_inputs
        )
    )


def _get_seen_at(
    toe_input: ToeInput,
    cvs_toe_input: ToeInput,
) -> Optional[datetime]:
    return (
        None
        if cvs_toe_input.seen_at is None
        else (
            cvs_toe_input.seen_at
            if cvs_toe_input.seen_at
            and toe_input.seen_at
            and cvs_toe_input.seen_at < toe_input.seen_at
            else toe_input.seen_at or cvs_toe_input.seen_at
        )
    )


async def update_toe_inputs(
    group_toe_inputs: Dict[int, ToeInput],
    cvs_group_toe_inputs: Dict[int, ToeInput],
) -> None:
    await collect(
        [
            toe_inputs_domain.update(
                current_value=group_toe_inputs[cvs_toe_input.get_hash()],
                attributes=ToeInputAttributesToUpdate(
                    attacked_at=cvs_toe_input.attacked_at,
                    attacked_by=cvs_toe_input.attacked_by,
                    be_present=cvs_toe_input.be_present,
                    first_attack_at=cvs_toe_input.first_attack_at,
                    seen_at=_get_seen_at(
                        group_toe_inputs[cvs_toe_input.get_hash()],
                        cvs_toe_input,
                    ),
                    seen_first_time_by=cvs_toe_input.seen_first_time_by,
                    unreliable_root_id=cvs_toe_input.unreliable_root_id,
                    clean_attacked_at=bool(cvs_toe_input.attacked_at is None),
                    clean_first_attack_at=bool(
                        cvs_toe_input.first_attack_at is None
                    ),
                    clean_seen_at=bool(
                        _get_seen_at(
                            group_toe_inputs[cvs_toe_input.get_hash()],
                            cvs_toe_input,
                        )
                        is None
                    ),
                ),
            )
            for cvs_toe_input in cvs_group_toe_inputs.values()
            if cvs_toe_input.get_hash() in group_toe_inputs
            and (
                cvs_toe_input.attacked_at,
                cvs_toe_input.attacked_by,
                cvs_toe_input.be_present,
                cvs_toe_input.first_attack_at,
                cvs_toe_input.seen_at,
                cvs_toe_input.seen_first_time_by,
                cvs_toe_input.unreliable_root_id,
            )
            != (
                group_toe_inputs[cvs_toe_input.get_hash()].attacked_at,
                group_toe_inputs[cvs_toe_input.get_hash()].attacked_by,
                group_toe_inputs[cvs_toe_input.get_hash()].be_present,
                group_toe_inputs[cvs_toe_input.get_hash()].first_attack_at,
                group_toe_inputs[cvs_toe_input.get_hash()].seen_at,
                group_toe_inputs[cvs_toe_input.get_hash()].seen_first_time_by,
                group_toe_inputs[cvs_toe_input.get_hash()].unreliable_root_id,
            )
        ]
    )


async def remove_toe_inputs(
    group_toe_inputs: Dict[int, ToeInput],
    cvs_group_toe_inputs: Dict[int, ToeInput],
) -> None:
    await collect(
        [
            toe_inputs_domain.remove(
                entry_point=toe_input.entry_point,
                component=toe_input.component,
                group_name=toe_input.group_name,
            )
            for toe_input in group_toe_inputs.values()
            if toe_input.get_hash() not in cvs_group_toe_inputs
        ]
    )


async def update_toe_inputs_from_csv(
    loaders: Dataloaders, group_name: str, inputs_csv_path: str
) -> None:
    group_roots: Tuple[RootItem, ...] = await loaders.group_roots.load(
        group_name
    )
    group_toe_inputs = {
        toe_input.get_hash(): toe_input
        for toe_input in await loaders.group_toe_inputs.load_nodes(
            GroupToeInputsRequest(group_name=group_name)
        )
    }
    group: Group = await loaders.group.load(group_name)
    cvs_group_toe_inputs = await in_process(
        _get_group_toe_inputs_from_cvs, inputs_csv_path, group, group_roots
    )
    await update_toe_inputs(group_toe_inputs, cvs_group_toe_inputs)
    await remove_toe_inputs(group_toe_inputs, cvs_group_toe_inputs)
    await add_toe_inputs(group_toe_inputs, cvs_group_toe_inputs)


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
