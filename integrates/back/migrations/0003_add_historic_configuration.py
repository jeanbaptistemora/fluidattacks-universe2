# type: ignore

# pylint: disable=invalid-name
"""This migration adds the 'historic_configuration' attribute to every project.

Before this change there were attributes 'has_forces', 'has_drills',
and 'type'.

After this change those attributes are placed into a list of historic
modifications so the backend can consume it and track it from there.

Another migration will be added later to delete the original fields,
once everything is well placed.
"""
import authz
import bugsnag
from dataloaders import (
    get_new_context,
)
from group_access import (
    domain as group_access_domain,
)
from groups import (
    dal as groups_dal,
)
import json
from newutils import (
    datetime as datetime_utils,
)
import os

STAGE: str = os.environ["STAGE"]


def log(message: str) -> None:
    print(message)
    bugsnag.notify(Exception(message), severity="info")


def guess_owner(group: str) -> str:
    loaders = get_new_context()
    all_users = group_access_domain.get_group_stakeholders_emails(
        loaders, group, active=True
    ) + group_access_domain.get_group_stakeholders_emails(
        loaders, group, active=False
    )

    possible_owner: str = "unknown"

    for email in all_users:
        if authz.get_group_level_role_legacy(email, group) == "customeradmin":
            possible_owner = email
            break

    return possible_owner


def main() -> None:
    log("Starting migration 0003")

    for group in groups_dal.get_all():
        # Attributes
        group_name = group["project_name"]
        has_forces = group.get("has_forces", False)
        has_drills = group.get("has_drills", False)
        type_ = group.get("type", "continuous")

        log(group_name)
        new_data = {
            "historic_configuration": [
                {
                    "date": datetime_utils.get_now_as_str(),
                    "has_forces": has_forces,
                    "has_drills": has_drills,
                    "requester": guess_owner(group_name),
                    "type": type_,
                }
            ]
        }
        new_data_str = json.dumps(new_data, indent=2)

        if STAGE == "test":
            log(f"new data would be: {new_data_str}")
        else:
            log(f"applied: {new_data_str}")
            groups_dal.update(group_name, new_data)

        log("---")


if __name__ == "__main__":
    main()
