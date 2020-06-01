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


def clone(
    subs_name: str,
    subs_path: str,
    clone_cmd: str = 'fluid resources --clone-from-customer-git',
) -> None:
    """Clone a subs_path."""
    _, output = run_command(clone_cmd, cwd=subs_path)
    print(f'INFO: git clone {subs_path}')
    print(f'      output:')
    print(textwrap.indent(output, ' ' * 16))

    os.makedirs(f'/git/{subs_name}', exist_ok=True)

    for repo_path in glob.glob(f'{subs_path}/fusion/*'):
        repo_name: str = os.path.basename(repo_path)
        repo_git_path = f'/git/{subs_name}/{repo_name}'
        if os.path.exists(repo_git_path):
            os.remove(repo_git_path)
        os.symlink(repo_path, repo_git_path)


def sync_to_s3(subs_path):
    _, output = run_command('fluid drills --push-repos', cwd=subs_path)
    print(f'INFO: sync to S3 {subs_path}')
    print(f'      output:')
    print(textwrap.indent(output, ' ' * 16))


def main() -> None:
    """Usual entry point."""
    subs_paths = glob.glob(f'/git/fluidattacks/services/groups/*')
    for subs_path in subs_paths:
        subs_name: str = os.path.basename(subs_path)

        clone(subs_name, subs_path)

        if os.path.exists(f'/git/{subs_name}') \
                and os.listdir(f'/git/{subs_name}'):
            sync_to_s3(subs_path)


if __name__ == '__main__':
    main()
