#!/usr/bin/env python3
"""Script to clone our repositories."""

import os
import sys

USER = os.environ['GITLAB_API_USER']
TOKEN = os.environ['GITLAB_API_TOKEN']


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
        sys.exit(status)


def main():
    """Usual entrypoint."""
    for repo in sys.argv[1:]:
        clone(repo)


if __name__ == '__main__':
    main()
