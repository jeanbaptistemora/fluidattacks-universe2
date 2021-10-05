from contextlib import (
    suppress,
)
import json
from model import (
    core_model,
)
from semver import (
    match,
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
)

# Constants
with open(f"{STATIC}/sca/npm.json", encoding="utf-8") as _FILE:
    DATABASE_NPM: Dict[str, Dict[str, List[str]]] = json.load(_FILE)

with open(f"{STATIC}/sca/maven.json", encoding="utf-8") as _FILE:
    DATABASE_MAVEN: Dict[str, Dict[str, List[str]]] = json.load(_FILE)

IGNORED_CHARS = str.maketrans("", "", "".join({"^", "~"}))


def does_version_match(version: str, condition: str) -> bool:
    """
    Given a version and a condition return True if version match condition.
    """
    result: bool = False
    with suppress(ValueError):
        result = match(version, condition)

    return result


def normalize(version: str) -> str:
    """Normalize a version so it contains major, minor and patch."""
    while version.count(".") < 2:
        version += ".0"
    return version


def remove_constraints(version: str) -> str:
    """Remove version constrans like `^`, `~` and `*`.

    These version constraints may be resolved to the latest or may not.
    It's better not to assume things and go conservative.
    """
    if version == "*":
        return "0"

    return (
        version.translate(IGNORED_CHARS)
        .replace(".*", ".0")
        .replace(".x", ".0")
    )


def query(
    platform: core_model.Platform,
    product: str,
    version: str,
) -> List[str]:
    """
    Search a product and a version in the database and return a list of CVE.
    """
    version = normalize(remove_constraints(version.strip().lower()))
    database = getattr(modules[__name__], f"DATABASE_{platform.value}")

    references: List[str] = [
        ref
        for ref, weak_versions in database.get(product.lower(), {}).items()
        for conditions in weak_versions
        if all(
            does_version_match(version, condition)
            for condition in conditions.split(",")
        )
    ]

    return references
