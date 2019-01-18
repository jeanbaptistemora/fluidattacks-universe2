""" script to clone our repositories """

import os

REPOS = (
    "autonomicmind/default",
    "autonomicmind/training",
    "fluidattacks/asserts",
    "fluidattacks/writeups",
    "fluidsignal/bwapp",
    "fluidsignal/continuous",
    "fluidsignal/default",
    "fluidsignal/integrates",
    "fluidsignal/serves",
    "fluidsignal/web",
)

USER = os.popen(f"vault read -field=analytics_gitlab_user secret/serves").read()
TOKEN = os.popen(f"vault read -field=analytics_gitlab_token secret/serves").read()

for repo in REPOS:
    os.system(f"git clone https://{USER}:{TOKEN}@gitlab.com/{repo}.git /git/{repo}")
