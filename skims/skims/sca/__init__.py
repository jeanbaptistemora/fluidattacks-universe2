from collections.abc import (
    Iterable,
)
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
from utils.function import (
    semver_match,
)
from utils.logs import (
    log_blocking,
)

Database = dict[str, dict[str, dict[str, str]]] | None

DATABASE: Database = None
DATABASE_PATCH: Database = None


async def get_advisories_from_s3(
    pkg_name: str, platform: str
) -> Iterable[tuple[str, str]] | None:
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
        ads: dict[str, str] = DATABASE.get(platform, {}).get(pkg_name, {})
        patch_ads: dict[str, str] = DATABASE_PATCH.get(platform, {}).get(
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
) -> Iterable[tuple[str, str]] | None:
    try:
        remote_ads: Iterable[Advisory] = await AdvisoriesLoader().load(
            (platform.lower(), pkg_name)
        )
        advisories: dict[str, str] = {}
        for advisory in remote_ads:
            updated_adv = {
                advisory.associated_advisory: advisory.vulnerable_version
            }
            if advisory.associated_advisory.startswith("GMS"):
                continue
            if advisory.associated_advisory in advisories:
                if advisory.source == PATCH_SRC:
                    advisories.update(updated_adv)
            else:
                advisories.update(updated_adv)
        return advisories.items()
    except Exception:  # pylint: disable=broad-except
        return None


async def get_remote_advisories(
    pkg_name: str, platform: str
) -> list[tuple[str, str]]:
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
) -> list[str]:
    product = product.lower()
    version = version.lower()

    advisories = await get_remote_advisories(product, platform.value)

    if advisories:
        vulnerabilities: list[str] = [
            ref
            for ref, constraints in advisories
            if semver_match(version, constraints)
        ]

        return vulnerabilities

    CTX.value_to_add.add(f"{platform.name} - {product}")
    return []
