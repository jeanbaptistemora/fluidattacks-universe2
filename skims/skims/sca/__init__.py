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
    STATIC,
    TOOLS_SEMVER_MATCH,
)
from utils.logs import (
    log_blocking,
)
from utils.system import (
    read_blocking,
)

with open(f"{STATIC}/sca/npm.json", encoding="utf-8") as _FILE:
    DATABASE_NPM: Dict[str, Dict[str, List[str]]] = json.load(_FILE)

with open(f"{STATIC}/sca/maven.json", encoding="utf-8") as _FILE:
    DATABASE_MAVEN: Dict[str, Dict[str, List[str]]] = json.load(_FILE)


def semver_match(left: str, right: str) -> bool:
    code, out, err = read_blocking(TOOLS_SEMVER_MATCH, left, right)

    if code == 0:
        data = json.loads(out)
        if data["success"]:
            return data["match"]

        log_blocking(
            "error", "Semver match %s to %s: %s", left, right, data["error"]
        )
    else:
        log_blocking("error", "Semver match %s to %s: %s", left, right, err)

    return False


def get_vulnerabilities(
    platform: core_model.Platform,
    product: str,
    version: str,
) -> List[str]:
    database = getattr(modules[__name__], f"DATABASE_{platform.value}")

    vulnerabilities: List[str] = [
        ref
        for ref, constraints in database.get(product.lower(), {}).items()
        for constraint in constraints
        if semver_match(version, constraint)
    ]

    return vulnerabilities
