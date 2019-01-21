""" generates the config file for tap-git """

import os
import json

SOURCE = "/git/fluidsignal/continuous"
TARGET = "/git"

BRANCHES = {}
with open(f"{TARGET}/../branches.json", "r") as file:
    BRANCHES = json.load(file)

FLUID_PROJ = (
    "autonomicmind",
    "fluidattacks",
    "fluidsignal"
)

# subscriptions with sub-subscriptions
NESTED = ("banistmo",)

CONFIG = {}
for proj in os.listdir(TARGET):
    if not proj in FLUID_PROJ and not proj in BRANCHES:
        print(f"ERROR|no {proj} in BRANCHES|")
        continue

    mailmap_path = f"{SOURCE}/subscriptions/{proj}/.mailmap"

    if any(subs in proj for subs in NESTED):
        nested_proj = proj.replace("-", "/")
        mailmap_path = f"{SOURCE}/subscriptions/{nested_proj}/.mailmap"

    proj_path = f"{TARGET}/{proj}"
    for repo in os.listdir(proj_path):
        if not proj in FLUID_PROJ and not repo in BRANCHES[proj]:
            print(f"ERROR|no {repo} in BRANCHES[{proj}]|")
            continue

        repo_path = f"{proj_path}/{repo}"
        repo_name = f"{proj}/{repo}"

        CONFIG[repo_name] = {
            "group": proj,
            "tag": proj,
            "location": repo_path,
            "branches": [
                "master" if proj in FLUID_PROJ else BRANCHES[proj][repo]
            ],
            ".mailmap": mailmap_path if os.path.exists(mailmap_path) else ""
        }

with open(f"{TARGET}/../config.json", "w") as file:
    json.dump(CONFIG, file, indent=2)
