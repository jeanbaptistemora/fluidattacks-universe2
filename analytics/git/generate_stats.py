#!/usr/bin/env python3

import os
import glob

from typing import List

from generate_config import FLUID_SUBS, get_repos_and_branches


def main():  # noqa
    """Usual entry point."""
    stats = {}
    branches = get_repos_and_branches(all_subs=True)

    for subs_path in glob.glob('/git/fluidattacks/services/groups/*'):
        subs_name = os.path.basename(subs_path)

        if subs_name in FLUID_SUBS:
            continue

        stats[subs_name] = {'CLONED': [], 'ERROR': []}
        for repo_name in branches[subs_name]:
            if os.path.exists(f'/git/{subs_name}/{repo_name}'):
                status = 'CLONED'
            else:
                status = 'ERROR'

            stats[subs_name][status].append(repo_name)

    # print the ones that were not cloned completely
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
            with open('repos_to_get_from_cache.lst', 'a') as handle:
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


if __name__ == '__main__':
    main()
