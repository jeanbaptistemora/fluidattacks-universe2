#!/usr/bin/env python3
""" generates the config file for tap-git """

import os
import json
import glob
import shutil
from urllib.parse import unquote

from typing import Dict, List

import yaml

# Local libraries
from clone_them import clone

# Constants
FLUID_GROUPS = (
    'autonomicmind',
    'fluidattacks',
    'fluidsignal',
)


CI_NODE_INDEX: int = int(os.environ.get('CI_NODE_INDEX', 1))
CI_NODE_TOTAL: int = int(os.environ.get('CI_NODE_TOTAL', 1))


def get_current_job_assignments(elements: list) -> list:
    return [
        element
        for index, element in enumerate(sorted(elements), start=1)
        if index % CI_NODE_TOTAL + 1 == CI_NODE_INDEX
    ]


def get_config_path(group: str) -> str:
    """Return the config path from the group name."""
    return (f'/git/fluidattacks/services/'
            f'groups/{group}/config/config.yml')


def get_customer_name(group: str) -> str:
    """Return the customer name for a group."""
    with open(get_config_path(group), 'r') as config_file:
        return yaml.safe_load(config_file).get('customer', '__')


def get_repos_and_branches(
        all_subs: bool = False) -> Dict[str, Dict[str, str]]:
    """Get the repo names and the branches from the config.yml."""
    branches: Dict[str, Dict[str, str]] = {}
    for subs_path in glob.glob('/git/fluidattacks/services/groups/*'
                               if all_subs else '/git/*'):
        group = os.path.basename(subs_path)
        if group in FLUID_GROUPS:
            continue

        branches[group] = {}

        with open(get_config_path(group), 'r') as config_file:
            yml_file = yaml.safe_load(config_file)

        for block in yml_file.get('code', []):
            if not block:
                continue

            this_branches = block.get('branches', [])

            if not this_branches:
                continue

            for repo_branch in this_branches:
                repo = unquote(repo_branch.rsplit('/')[-2])
                branch = unquote(repo_branch.rsplit('/')[-1])
                branches[group].update({repo: branch})

    return branches


def main():
    """Usual entry point."""
    services_assignments: List[str] = get_current_job_assignments(
        glob.glob('/git/fluidattacks/services/groups/*')
    )
    fluid_assignments: List[str] = get_current_job_assignments([
        'autonomicmind',
        'fluidattacks',
    ])

    # Clone the repositories for this job
    for group_path in services_assignments:
        group = os.path.basename(group_path)
        clone(group, group_path, clone_cmd='fluid drills --pull-repos')

    branches: Dict[str, Dict[str, str]] = get_repos_and_branches()

    # Generate a config file for the groups in this job
    config = []
    for group_path in fluid_assignments + services_assignments:
        group = os.path.basename(group_path)

        organization = (
            'fluidattacks'
            if group in FLUID_GROUPS
            else get_customer_name(group)
        )

        for repo_path in glob.glob(f'/git/{group}/*'):
            repo = os.path.basename(repo_path)

            shutil.copyfile(
                '/git/fluidattacks/services/.groups-mailmap',
                f'{repo_path}/.mailmap',
            )

            if group in FLUID_GROUPS or repo in branches[group]:
                config.append(
                    {
                        'organization': organization,
                        'subscription': group,
                        'repository': repo,
                        'location': repo_path,
                        'branches': [
                            'master' if group in FLUID_GROUPS
                            else branches[group][repo]
                        ],
                    }
                )
            else:
                print(f'ERROR: {repo} not in branches[{group}]')
                print(json.dumps(branches[group], indent=2))

    with open(f'./config.json', 'w') as file:
        json.dump(config, file, indent=2)

    print(json.dumps(config, indent=2))


if __name__ == '__main__':
    main()
