#!/usr/bin/env python3
""" generates the config file for tap-git """

import os
import json
import glob
import shutil
import textwrap
from urllib.parse import unquote

from typing import Dict

import yaml


# Constants
FLUID_SUBS = (
    'autonomicmind',
    'fluidattacks',
    'fluidsignal',
)


def get_config_path(subs_name: str) -> str:
    """Return the config path from the group name."""
    return (f'/git/fluidattacks/services/'
            f'groups/{subs_name}/config/config.yml')


def get_customer_name(subs_name: str) -> str:
    """Return the customer name for a group."""
    with open(get_config_path(subs_name), 'r') as config_file:
        return yaml.safe_load(config_file).get('customer', '__')


def get_repos_and_branches(
        all_subs: bool = False) -> Dict[str, Dict[str, str]]:
    """Get the repo names and the branches from the config.yml."""
    branches: Dict[str, Dict[str, str]] = {}
    for subs_path in glob.glob('/git/fluidattacks/services/groups/*'
                               if all_subs else '/git/*'):
        subs_name = os.path.basename(subs_path)
        if subs_name in FLUID_SUBS:
            continue

        branches[subs_name] = {}

        with open(get_config_path(subs_name), 'r') as config_file:
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
                branches[subs_name].update({repo: branch})

    return branches


def main():
    """Usual entry point."""
    config = []
    branches: Dict[str, Dict[str, str]] = get_repos_and_branches()

    for subs_path in glob.glob('/git/*'):
        subs_name = os.path.basename(subs_path)

        if subs_name in FLUID_SUBS:
            organization = 'fluidattacks'
        else:
            organization = get_customer_name(subs_name)

        for repo_path in glob.glob(f'{subs_path}/*'):
            repo_name = os.path.basename(repo_path)

            mailmap_target_path = f'{repo_path}/.mailmap'
            mailmap_path = (f'/git/fluidattacks/'
                            f'services/groups/{subs_name}/.mailmap')
            if os.path.exists(mailmap_path):
                shutil.copyfile(mailmap_path, mailmap_target_path)

            if subs_name in FLUID_SUBS or repo_name in branches[subs_name]:
                config.append(
                    {
                        'organization': organization,
                        'subscription': subs_name,
                        'repository': repo_name,
                        'location': repo_path,
                        'branches': [
                            'master' if subs_name in FLUID_SUBS
                            else branches[subs_name][repo_name]
                        ],
                    }
                )
            else:
                print(f'ERROR: {repo_name} not in branches[{subs_name}]')
                print(textwrap.indent(
                    json.dumps(branches[subs_name], indent=2), ' ' * 8))

    with open(f'./config.json', 'w') as file:
        json.dump(config, file, indent=2)

    print(json.dumps(config, indent=2))


if __name__ == '__main__':
    main()
