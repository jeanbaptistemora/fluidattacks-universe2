#!/usr/bin/env python3

import os
import glob

from typing import List, Dict, Tuple

from generate_config import FLUID_GROUPS, get_repos_and_branches

StatsType = Dict[str, Dict[str, List[str]]]


def add_stats(
    old_stats: StatsType,
    subs_name: str,
    branches: List[str],
) -> StatsType:

    stats = old_stats

    stats[subs_name] = {'CLONED': [], 'ERROR': []}
    for repo_name in branches:
        if os.path.exists(f'/git/{subs_name}/{repo_name}'):
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

        if int(subs_total_repos_count) > 0 \
                and int(subs_cloned_repos_count) == 0:
            with open('subs_to_get_from_s3.lst', 'a') as handle:
                handle.write(subs)
                handle.write('\n')

        if subs_error_repos:
            messages.append('  - {:^22s} {:>3.0f}/{:>3.0f}'.format(
                subs, subs_cloned_repos_count, subs_total_repos_count))

            if subs_cloned_repos:
                error_messages.append(f'  {subs}')
                for repo in subs_error_repos:
                    error_messages.append(f'    - {repo}')

    print('Git pipeline summary:')
    for message in messages:
        print(message)

    if messages:
        print('Git pipeline errors:')
        for message_error in error_messages:
            print(message_error)


def main():  # noqa
    """Usual entry point."""
    stats: StatsType = {}
    branches = get_repos_and_branches(all_subs=True)

    for subs_path in glob.glob('/git/fluidattacks/services/groups/*'):
        subs_name = os.path.basename(subs_path)

        if subs_name in FLUID_GROUPS:
            continue

        stats = add_stats(stats, subs_name, branches[subs_name])

    print_stats(stats)


if __name__ == '__main__':
    main()
