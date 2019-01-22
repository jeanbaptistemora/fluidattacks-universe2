""" generates the config file for tap-git """

import os
import json

import yaml # pylint: disable=import-error

SOURCE = "/git/fluidsignal/continuous"
TARGET = "/git"

def get_organization(yml_path):
    """ returns the -customer- tag in the config.yml """

    with open(yml_path, "r") as config_file:
        return yaml.load(config_file).get("customer", "__")

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

CONFIG = []
for proj in os.listdir(TARGET):
    if not proj in FLUID_PROJ and not proj in BRANCHES:
        print(f"ERROR|no {proj} in BRANCHES|")
        continue

    project_path = f"{SOURCE}/subscriptions/{proj}"

    if any(subs in proj for subs in NESTED):
        nested_proj = proj.replace("-", "/")
        project_path = f"{SOURCE}/subscriptions/{nested_proj}"

    ymlconf_path = f"{project_path}/config.yml"
    mailmap_path = f"{project_path}/.mailmap"

    if not os.path.exists(mailmap_path):
        mailmap_path = ""
    if not os.path.exists(ymlconf_path):
        ymlconf_path = ""

    subscription = proj.split("-")[0]
    organization = "__"

    if proj in FLUID_PROJ:
        organization = "fluidattacks"
    elif ymlconf_path:
        organization = get_organization(ymlconf_path)

    proj_path = f"{TARGET}/{proj}"
    for repo in os.listdir(proj_path):
        if not proj in FLUID_PROJ and not repo in BRANCHES[proj]:
            print(f"ERROR|no {repo} in BRANCHES[{proj}]|")
            continue

        repo_path = f"{proj_path}/{repo}"
        repo_name = f"{proj}/{repo}"

        CONFIG.append(
            {
                "organization":  organization,
                "subscription": subscription,
                "repository": repo,
                "location": repo_path,
                "branches": [
                    "master" if proj in FLUID_PROJ else BRANCHES[proj][repo]
                ],
                ".mailmap": mailmap_path
            }
        )

with open(f"{TARGET}/../config.json", "w") as file:
    json.dump(CONFIG, file, indent=2)

print(json.dumps(CONFIG, indent=2))
