#!/usr/bin/env python3

import os

from typing import List, Any

import yaml
import slack


# path to the continuous repo
CONTINUOUS: str = "/git/fluidsignal/continuous"


def slack__send_message(header: str, message: List[str]) -> None:
    """Send a message to the Analytics channel."""
    slack_token = os.popen(
        "vault read -field=analytics_slack_token secret/serves").read()
    body: str = "\n".join(message)
    slack.WebClient(token=slack_token).chat_postMessage(
        text=f"*{header}*\n\n```\n{body}\n```",
        channel="#analytics",
        mrkdwn=True)


def get_subs_nrepos(subs_name: str) -> int:
    """Parse the config.yml for a subscription, return the number of repos."""
    subs_path: str = f"{CONTINUOUS}/subscriptions/{subs_name}"
    with open(f"{subs_path}/config/config.yml", "r") as config_file:
        yml: Any = yaml.safe_load(config_file)
        yml__code: Any = yml.get("code", {})
        yml__code__branches: List[str] = yml__code.get("branches", [])
    return len(yml__code__branches)


def main():
    """Usual entry point."""

    # filther the clone_them log to produce an input for this script
    os.system((
        r"cat clone_them.log"
        r"| grep 'INFO|STATS'"
        r"| sed -E 's/INFO\|STATS\|\/git\/fluidsignal\/continuous"
        r"\/subscriptions\/(.*)\|(.*)\|/\1 \2/g'"
        r"> clone_them.log.filtered"))

    # get the name and the cloned repositories
    with open("clone_them.log.filtered") as log_file:
        name__cloned_repos = [line.split() for line in log_file.readlines()]

    # print the ones that were not cloned completely
    header: str = "STATS: clone_them.py"
    message: List[str] = []
    for subs_name, subs_cloned_repos in name__cloned_repos:
        subs_total_repos: str = str(get_subs_nrepos(subs_name))
        if not subs_cloned_repos == subs_total_repos:
            message.append("{:^22s} {:>3s}/{:>3s}".format(
                subs_name, subs_cloned_repos, subs_total_repos))
    slack__send_message(header, message)


if __name__ == "__main__":
    main()
