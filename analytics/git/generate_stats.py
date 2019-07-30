#!/usr/bin/env python3

import os
import glob

from typing import List

import slack

from generate_config import FLUID_SUBS, get_repos_and_branches


def slack__send_message(header: str, message: List[str]) -> None:
    """Send a message to the Analytics channel."""
    slack_token = os.popen(
        'vault read -field=analytics_slack_token secret/serves').read()
    body: str = '\n'.join(message)
    text: str = f'*{header}*\n\n```\n{body}\n```'
    slack.WebClient(token=slack_token).chat_postMessage(
        text=text, channel='#analytics', mrkdwn=True)


def main():  # noqa
    """Usual entry point."""
    stats = {}
    branches = get_repos_and_branches(all_subs=True)

    for subs_path in glob.glob('/git/fluidsignal/continuous/subscriptions/*'):
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
    message: List[str] = []
    message_errors: List[str] = []

    send_errors: bool = False
    for subs in stats:
        subs_cloned_repos = stats[subs].get('CLONED', [])
        subs_error_repos = stats[subs].get('ERROR', [])
        subs_cloned_repos_count = len(subs_cloned_repos)
        subs_error_repos_count = len(subs_error_repos)
        subs_total_repos_count: str = \
            subs_cloned_repos_count + subs_error_repos_count

        if subs_error_repos:
            message.append('{:^22s} {:>3.0f}/{:>3.0f}'.format(
                subs, subs_cloned_repos_count, subs_total_repos_count))

        if subs_error_repos:
            send_errors = True
            message_errors.append(f'  {subs}:')
            if subs_cloned_repos:
                for repo in subs_error_repos:
                    message_errors.append(f'    {repo}')
            else:
                message_errors.append(f'    all')

    slack__send_message('Git pipeline summary', message)
    if send_errors:
        slack__send_message('Git pipeline errors', message_errors)


if __name__ == '__main__':
    main()
