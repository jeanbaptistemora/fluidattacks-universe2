#!/usr/bin/env python3
"""Clone or update repositories for groups in the services repo."""

import os
import glob
import textwrap
import subprocess
from urllib.parse import unquote
from itertools import zip_longest
from typing import List, Dict, Tuple

from generate_config import get_repos_and_branches

import ruamel.yaml as yaml
import bugsnag


RELEASE_STAGE = os.environ.get('ENVIRONMENT_NAME', 'development')
JOB_ID = os.environ.get('CI_JOB_ID', 'LOCAL')
CI_NODE_INDEX = int(os.environ.get('CI_JOB_ID', '1'))
CI_NODE_TOTAL = int(os.environ.get('CI_JOB_ID', '1'))


bugsnag.configure(
    api_key='13748c4b5f6807a89f327c0f54fe6c7a',
    release_stage=RELEASE_STAGE,
)
bugsnag.start_session()
bugsnag.send_sessions()


StatsType = Dict[str, Dict[str, List[str]]]


def chunk_dicc(index_group: int, total_groups: int, to_split):
    """
    return the indexed chunk

    Use this function to regroup dictionaries by chunks.
    recommended for CI parallel jobs
    """
    # https://docs.python.org/3.7/library/itertools.html#itertools-recipes
    def grouper(iterable, size, fillvalue=None):
        "Collect data into fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * size
        return zip_longest(*args, fillvalue=fillvalue)

    size = len(to_split) // total_groups
    size_group_1 = (len(to_split) - size * total_groups) * (size + 1)
    keys = sorted(to_split)
    chunks_1 = list(grouper(keys[: size_group_1], size + 1))
    chunks_2 = list(grouper(keys[size_group_1:], size))
    chunks = chunks_1 + chunks_2

    if index_group > len(chunks):
        return {}
    return {key: to_split[key] for key in chunks[index_group - 1]}


BRANCHES = chunk_dicc(
    CI_NODE_INDEX,
    CI_NODE_TOTAL,
    get_repos_and_branches(all_subs=True)
)


def run_command(cmd: str, cwd: str) -> Tuple[int, str]:
    """Run a command and return exit code and output."""
    # pylint: disable=subprocess-run-check
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        env=os.environ
    )
    return proc.returncode, proc.stdout


def add_stats(
    old_stats: StatsType,
    subs_name: str,
) -> StatsType:

    stats = old_stats

    stats[subs_name] = {'CLONED': [], 'ERROR': []}
    local_branches = [
        unquote(os.path.basename(path))
        for path in glob.glob(f'/git/{subs_name}/*')
    ]
    for repo_name in BRANCHES[subs_name]:
        if repo_name in local_branches:
            status = 'CLONED'
        else:
            status = 'ERROR'

        stats[subs_name][status].append(repo_name)

    return stats


def separate_results_stats(
    stats: StatsType,
) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:

    cloned_repos: Dict[str, List[str]] = {}
    error_repos: Dict[str, List[str]] = {}

    for subs in sorted(stats):
        subs_cloned_repos = stats[subs].get('CLONED', [])
        subs_error_repos = stats[subs].get('ERROR', [])
        if subs_cloned_repos:
            cloned_repos[subs] = subs_cloned_repos
        if subs_error_repos:
            error_repos[subs] = subs_error_repos

    return cloned_repos, error_repos


def print_stats(stats: StatsType) -> None:
    """ print the ones that were not cloned completely """
    messages: List[str] = []
    error_messages: List[str] = []

    for subs in sorted(stats):
        subs_cloned_repos = stats[subs].get('CLONED', [])
        subs_error_repos = stats[subs].get('ERROR', [])
        subs_cloned_repos_count: float = float(len(subs_cloned_repos))
        subs_error_repos_count: float = float(len(subs_error_repos))
        subs_total_repos_count: float = \
            subs_cloned_repos_count + subs_error_repos_count

        if subs_error_repos:
            messages.append('  - {:^22s} {:>3.0f}/{:>3.0f}'.format(
                subs, subs_cloned_repos_count, subs_total_repos_count))

            if subs_cloned_repos:
                error_messages.append(f'  {subs}')
                for repo in subs_error_repos:
                    error_messages.append(f'    - {repo}')

    print('Git pipeline summary:')
    if messages:
        for message in messages:
            print(message)

        print('Git pipeline errors:')
        for message_error in error_messages:
            print(message_error)
    else:
        print('- OK')


def clone(
    subs_name: str,
    subs_path: str,
    clone_cmd: str = 'melts resources --clone-from-customer-git',
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
    _, output = run_command('melts drills --push-repos', cwd=subs_path)
    print(f'INFO: sync to S3 {subs_path}')
    print('      output:')
    print(textwrap.indent(output, ' ' * 16))


def all_repos_use_vpn(subs_path) -> bool:
    with open(f'{subs_path}/config/config.yml') as config_handle:
        code_config = yaml.safe_load(config_handle.read()).get('code', [])

    for repo in code_config:
        if not repo['vpn']:
            return False

    return True


def main() -> None:
    """Usual entry point."""
    # This is to load melts dependencies before start cloning repos
    run_command('melts --help', cwd='/git/fluidattacks/services/groups/')

    subs_paths = [
        f'/git/fluidattacks/services/groups/{rep}'
        for rep in sorted(BRANCHES)
    ]
    stats: StatsType = {}
    diskusage: List[str] = []

    for subs_path in subs_paths:
        subs_name: str = os.path.basename(subs_path)

        if all_repos_use_vpn(subs_path):
            print('[INFO] This group is cloning from S3')
            clone(subs_name, subs_path, 'melts drills --pull-repos')
        else:
            clone(subs_name, subs_path)

        if (os.path.exists(f'/git/{subs_name}') and
                os.listdir(f'/git/{subs_name}')):
            sync_to_s3(subs_path)

        stats = add_stats(stats, subs_name)
        _, output = run_command('du -sh', cwd='/git/')
        diskusage.append(output.split()[0])
        print(diskusage)

        run_command('rm -rf */* */.*', cwd=f'{subs_path}/fusion/')

    print_stats(stats)
    _, error_repos = separate_results_stats(stats)

    if error_repos:
        bugsnag.notify(
            Exception('Some repositories failed to be cloned'),
            severity='error',
            meta_data={
                'JOB_INFO': {
                    'ENVIRONMENT': RELEASE_STAGE,
                    'CI_JOB_ID': JOB_ID,
                    'CI_NODE_INDEX': CI_NODE_INDEX,
                    'CI_NODE_TOTAL': CI_NODE_TOTAL
                },
                'FAILED_REPOS':  error_repos,
            },
        )


if __name__ == '__main__':
    main()
