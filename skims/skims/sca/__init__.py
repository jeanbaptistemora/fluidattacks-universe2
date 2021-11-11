import json
from model import (
    core_model,
)
from sys import (
    modules,
)
from typing import (
    Dict,
    List,
)
from utils.ctx import (
    CTX,
    STATIC,
    TOOLS_SEMVER_MATCH,
)
from utils.logs import (
    log_blocking,
)
from utils.system import (
    read_blocking,
)

Database = Dict[str, Dict[str, List[str]]]


def _validate(database: Database) -> Database:
    for project, vulnerabilities in database.items():

        if project != project.lower():
            raise ValueError(f"Not lowercase project: {project}")

        for versions in vulnerabilities.values():
            for version in versions:
                if version != version.lower():
                    raise ValueError(f"Not lowercase: {version}")

    return database


with open(f"{STATIC}/sca/npm.json", encoding="utf-8") as _FILE:
    DATABASE_NPM: Database = _validate(json.load(_FILE))

with open(f"{STATIC}/sca/maven.json", encoding="utf-8") as _FILE:
    DATABASE_MAVEN: Database = _validate(json.load(_FILE))

with open(f"{STATIC}/sca/nuget.json", encoding="utf-8") as _FILE:
    DATABASE_NUGET: Database = _validate(json.load(_FILE))


def semver_match(left: str, right: str) -> bool:
    code, out, _ = read_blocking(TOOLS_SEMVER_MATCH, left, right)

    if code == 0:
        data = json.loads(out)
        if data["success"]:
            return data["match"]

        log_blocking(
            "error", "Semver match %s to %s: %s", left, right, data["error"]
        )
    else:
        log_blocking("error", "Semver match %s to %s", left, right)

    return False


def get_vulnerabilities(
    platform: core_model.Platform,
    product: str,
    version: str,
) -> List[str]:
    database = getattr(modules[__name__], f"DATABASE_{platform.value}")
    product = product.lower()
    version = version.lower()

    if product in database:
        vulnerabilities: List[str] = [
            ref
            for ref, constraints in database[product].items()
            if semver_match(version, constraints)
        ]

        return vulnerabilities

    CTX.value_to_add.add(f"{platform.name} - {product}")
    return []
