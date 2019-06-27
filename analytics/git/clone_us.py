#!/usr/bin/env python3
"""Script to clone our repositories."""

import os

USER = os.popen(
    f"vault read -field=analytics_gitlab_user secret/serves").read()
TOKEN = os.popen(
    f"vault read -field=analytics_gitlab_token secret/serves").read()
TARGET = "/git"

REPOS = (
    "autonomicmind/default",
    "autonomicmind/training",
    "fluidattacks/web",
    "fluidattacks/default",
    "fluidattacks/asserts",
    "fluidattacks/writeups",
    "fluidattacks/integrates",
    "fluidattacks/bwapp",
    "fluidsignal/serves",
    "fluidsignal/default",
    "fluidsignal/continuous",
)

for repo in REPOS:
    dest = f"{TARGET}/{repo}"
    if os.path.isdir(dest):
        # Update the repository
        status = os.system(
            f"git -C '{dest}' pull --autostash --rebase origin master")
    else:
        # Clone the repository
        status = os.system((
            f"git clone --branch master --single-branch"
            f"  https://{USER}:{TOKEN}@gitlab.com/{repo}.git '{dest}'"))
    if status:
        print(f"Clone/update of {repo} exit with status code {status}")
        exit(status)
