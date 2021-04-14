"""This migration adds the 'historic_configuration' attribute to every project.

Before this change there were attributes 'has_forces', 'has_drills',
and 'type'.

After this change those attributes are placed into a list of historic
modifications so the backend can consume it and track it from there.

Another migration will be added later to delete the original fields,
once everything is well placed.
"""

import json
import os
from datetime import datetime

import bugsnag
from backend import util
from backend.dal import project as project_dal
from backend import authz
from group_access import domain as group_access_domain


STAGE: str = os.environ['STAGE']


def log(message: str) -> None:
    print(message)
    bugsnag.notify(Exception(message), severity='info')


def guess_owner(group: str) -> str:
    all_users = (
        group_access_domain.get_group_users(group, active=True) +
        group_access_domain.get_group_users(group, active=False)
    )

    possible_owner: str = 'unknown'

    for email in all_users:
        if authz.get_group_level_role(email, group) == 'customeradmin':
            possible_owner = email
            break

    return possible_owner


def main() -> None:
    log('Starting migration 0003')

    for group in project_dal.get_all():
        # Attributes
        group_name = group['project_name']
        has_forces = group.get('has_forces', False)
        has_drills = group.get('has_drills', False)
        type_ = group.get('type', 'continuous')

        log(group_name)
        new_data = {
            'historic_configuration': [{
                'date': util.get_current_time_as_iso_str(),
                'has_forces': has_forces,
                'has_drills': has_drills,
                'requester': guess_owner(group_name),
                'type': type_,
            }]
        }
        new_data_str = json.dumps(new_data, indent=2)

        if STAGE == 'test':
            log(f'new data would be: {new_data_str}')
        else:
            log(f'applied: {new_data_str}')
            project_dal.update(group_name, new_data)

        log('---')


if __name__ == '__main__':
    main()
