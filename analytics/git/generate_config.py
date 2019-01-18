""" generates the config file for tap-git """

import os
import json

TARGET = "/git"

BRANCHES = {}
with open(f"{TARGET}/../branches.json", "r") as file:
    BRANCHES = json.load(file)

FLUID_PROJ = (
    "autonomicmind",
    "fluidattacks",
    "fluidsignal"
)

CONFIG = {}
for proj in os.listdir(TARGET):
    proj_path = f"{TARGET}/{proj}"
    for repo in os.listdir(proj_path):
        repo_path = f"{proj_path}/{repo}"
        repo_name = f"{proj}/{repo}"
        mailmap_path = f"{repo_path}/.mailmap"
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
