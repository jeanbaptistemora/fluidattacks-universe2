#!/usr/bin/env python3
"""Clone or update repositories for groups in the services repo."""

import os
import glob
import textwrap
import subprocess

from typing import Tuple


def run_command(cmd: str, cwd: str) -> Tuple[int, str]:
    """Run a command and return exit code and output."""
    # pylint: disable=subprocess-run-check
    proc = subprocess.run(cmd,
                          cwd=cwd,
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          universal_newlines=True,
                          env=os.environ)
    return proc.returncode, proc.stdout


def clone(subs_path) -> None:
    """Clone a subs_path."""
    _, output = run_command(
        'fluid resources --clone-from-customer-git', cwd=subs_path)
    print(f'INFO: {subs_path}')
    print(f'      output:')
    print(textwrap.indent(output, ' ' * 16))

    subs_name: str = os.path.basename(subs_path)
    os.makedirs(f'/git/{subs_name}', exist_ok=True)

    for repo_path in glob.glob(f'{subs_path}/fusion/*'):
        repo_git_path = f'/git/{subs_name}/{os.path.basename(repo_path)}'
        if os.path.exists(repo_git_path):
            os.remove(repo_git_path)
        os.symlink(repo_path, repo_git_path)


def sync_to_s3(subs_path):
    _, output = run_command('fluid drills --push-repos', cwd=subs_path)
    print(f'INFO: {subs_path}')
    print(f'      output:')
    print(textwrap.indent(output, ' ' * 16))


def open_vpn(subs_path) -> None:
    """Clone a subs_path which requires a vpn connection."""
    _, output = run_command('yes 2 | fluid drills --vpn', cwd=subs_path)
    print(f'INFO: {subs_path}')
    print(f'      output:')
    print(textwrap.indent(output, ' ' * 16))


def main() -> None:
    """Usual entry point."""
    subs_paths = glob.glob(f'/git/fluidattacks/services/groups/*')
    for subs_path in subs_paths:
        clone(subs_path)
        sync_to_s3(subs_path)


if __name__ == '__main__':
    main()
