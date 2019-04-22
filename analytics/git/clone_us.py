#!/usr/bin/env python3
"""Script to clone our repositories."""

import os

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

USER = os.popen(
    f"vault read -field=analytics_gitlab_user secret/serves").read()
TOKEN = os.popen(
    f"vault read -field=analytics_gitlab_token secret/serves").read()

for repo in REPOS:
    status = os.system((
        f"git clone"
        f"  https://{USER}:{TOKEN}@gitlab.com/{repo}.git"
        f"  {TARGET}/{repo}"))
    if status:
        print(f"Clone of {repo} exit with status code {status}")
        exit(status)
