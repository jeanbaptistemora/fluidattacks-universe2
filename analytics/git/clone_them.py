#!/usr/bin/env python3
"""Clone or update repositories for subscriptions in the continuous repo."""

import os
import glob
import textwrap
import subprocess
from multiprocessing import cpu_count
from multiprocessing.pool import Pool

from typing import Tuple


def run_command(cmd: str, cwd: str) -> Tuple[int, str]:
    """Run a command and return exit code and output."""
    proc = subprocess.run(cmd,
                          cwd=cwd,
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          universal_newlines=True)
    return proc.returncode, proc.stdout


def clone(subs_path) -> None:
    """Clone a subs_path."""
    _, output = run_command('../../tools/repo-cloning.py', cwd=subs_path)
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


def main() -> None:
    """Usual entry point."""
    subs_paths = glob.glob(f'/git/fluidsignal/continuous/subscriptions/*')
    # Let's spam a little the context switching
    # The clone is an IOBound operation
    with Pool(processes=cpu_count() * 8) as workers:
        workers.map(clone, subs_paths)


if __name__ == '__main__':
    main()
