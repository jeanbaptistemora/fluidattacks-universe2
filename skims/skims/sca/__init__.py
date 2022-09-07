# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ctx import (
    CTX,
    STATIC,
)
from db_model.advisories.constants import (
    PATCH_SRC,
)
from db_model.advisories.get import (
    AdvisoriesLoader,
)
from db_model.advisories.types import (
    Advisory,
)
import json
from model import (
    core_model,
)
from typing import (
    Dict,
    Iterable,
    List,
    Tuple,
)
from utils.function import (
    semver_match,
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

with open(f"{STATIC}/sca/pip.json", encoding="utf-8") as _FILE:
    DATABASE_PIP: Database = _validate(json.load(_FILE))


async def get_remote_advisories(
    pkg_name: str, platform: str
) -> List[Tuple[str, str]]:
    remote_ads: Iterable[Advisory] = await AdvisoriesLoader().load(
        (platform.lower(), pkg_name)
    )
    advisories: Dict[str, str] = {}
    for advisory in remote_ads:
        if advisory.associated_advisory.startswith("GMS"):
            continue
        if advisory.associated_advisory in advisories:
            if advisory.source == PATCH_SRC:
                advisories.update(
                    {advisory.associated_advisory: advisory.vulnerable_version}
                )
        else:
            advisories.update(
                {advisory.associated_advisory: advisory.vulnerable_version}
            )
    return sorted(advisories.items())


async def get_vulnerabilities(
    platform: core_model.Platform,
    product: str,
    version: str,
) -> List[str]:
    product = product.lower()
    version = version.lower()

    advisories = await get_remote_advisories(product, platform.value)

    if advisories:
        vulnerabilities: List[str] = [
            ref
            for ref, constraints in advisories
            if semver_match(version, constraints)
        ]

        return vulnerabilities

    CTX.value_to_add.add(f"{platform.name} - {product}")
    return []
