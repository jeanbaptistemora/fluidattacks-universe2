#!/usr/bin/env python3
"""Script to clone our repositories."""

import os
from multiprocessing import cpu_count
from multiprocessing.pool import Pool

USER = os.popen(
    f'vault read -field=analytics_gitlab_user secret/serves').read()
TOKEN = os.popen(
    f'vault read -field=analytics_gitlab_token secret/serves').read()


def clone(repo) -> None:
    """Clone a dest."""
    dest = f'/git/{repo}'
    if os.path.isdir(dest):
        # Update the repository
        status = os.system(
            f'git -C \'{dest}\' pull --autostash --rebase origin master')
    else:
        # Clone the repository
        status = os.system((
            f'git clone --branch master --single-branch'
            f'  https://{USER}:{TOKEN}@gitlab.com/{repo}.git \'{dest}\''))
    if status:
        print(f'Clone/update of {repo} exit with status code {status}')
        exit(status)


def main():
    """Usual entrypoint."""
    with Pool(processes=cpu_count()) as workers:
        workers.map(clone, [
            'autonomicmind/default',
            'autonomicmind/training',
            'fluidattacks/web',
            'fluidattacks/public',
            'fluidattacks/asserts',
            'fluidattacks/writeups',
            'fluidattacks/integrates',
            'fluidattacks/bwapp',
            'fluidattacks/serves',
            'fluidattacks/continuous',
            'fluidsignal/default',
        ])


if __name__ == '__main__':
    main()
