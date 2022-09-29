# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ctx import (
    CTX,
)
from db_model.advisories.constants import (
    PATCH_SRC,
    SUPPORTED_PLATFORMS,
)
from db_model.advisories.get import (
    AdvisoriesLoader,
)
from db_model.advisories.types import (
    Advisory,
)
from model import (
    core_model,
)
from s3.operations import (
    download_advisories,
)
from s3.resource import (
    s3_shutdown,
    s3_start_resource,
)
from typing import (
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
)
from utils.function import (
    semver_match,
)
from utils.logs import (
    log_blocking,
)

Database = Optional[Dict[str, Dict[str, Dict[str, str]]]]

DATABASE: Database = None
DATABASE_PATCH: Database = None


async def get_advisories_from_s3(
    pkg_name: str, platform: str
) -> Optional[Iterable[Tuple[str, str]]]:
    try:
        # pylint: disable=global-statement
        global DATABASE, DATABASE_PATCH
        if DATABASE is None or DATABASE_PATCH is None:
            await s3_start_resource(is_public=True)
            s3_advisories, s3_patch_advisories = await download_advisories(
                needed_platforms=SUPPORTED_PLATFORMS
            )
            DATABASE = s3_advisories
            DATABASE_PATCH = s3_patch_advisories
            await s3_shutdown()
        ads: Dict[str, str] = DATABASE.get(platform, {}).get(pkg_name, {})
        patch_ads: Dict[str, str] = DATABASE_PATCH.get(platform, {}).get(
            pkg_name, {}
        )
        ads.update(patch_ads)
        no_gms_ads = {
            key: value
            for key, value in ads.items()
            if not key.startswith("GMS")
        }
        return no_gms_ads.items()
    except Exception:  # pylint: disable=broad-except
        log_blocking(
            "error",
            "Couldn't download advisories from s3 bucket",
        )
        return None


async def get_advisories_from_dynamodb(
    pkg_name: str, platform: str
) -> Optional[Iterable[Tuple[str, str]]]:
    try:
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
                        {
                            advisory.associated_advisory: advisory.vulnerable_version  # noqa
                        }
                    )
            else:
                advisories.update(
                    {advisory.associated_advisory: advisory.vulnerable_version}
                )
        return advisories.items()
    except Exception:  # pylint: disable=broad-except
        return None


async def get_remote_advisories(
    pkg_name: str, platform: str
) -> List[Tuple[str, str]]:
    if (
        DATABASE is None
        and (
            advisories := await get_advisories_from_dynamodb(
                pkg_name, platform.lower()
            )
        )
        is not None
    ):
        return sorted(advisories)
    if (
        s3_advisories := await get_advisories_from_s3(
            pkg_name, platform.lower()
        )
    ) is not None:
        return sorted(s3_advisories)
    return []


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
