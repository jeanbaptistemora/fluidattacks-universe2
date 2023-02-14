from .types import (
    Advisory,
)
from custom_exceptions import (
    _SingleMessageException,
    InvalidSeverity,
    InvalidVulnerableVersion,
)
from datetime import (
    datetime,
)
from db_model.advisories.constants import (
    PATCH_SRC,
)
from dynamodb.types import (
    Item,
)
from utils.function import (
    semver_match,
)
from utils.logs import (
    log_blocking,
)

VALID_RANGES = ("=", "<", ">", ">=", "<=")
CVSS_BASE_METRICS: dict[str, tuple[str, ...]] = {
    "AV": ("N", "A", "L", "P"),
    "AC": ("L", "H"),
    "PR": ("N", "L", "H"),
    "UI": ("N", "R"),
    "S": ("U", "C"),
    "C": ("H", "L", "N"),
    "I": ("H", "L", "N"),
    "A": ("H", "L", "N"),
}


def format_item_to_advisory(item: Item) -> Advisory:
    return Advisory(
        associated_advisory=item["associated_advisory"],
        package_name=item["package_name"],
        package_manager=item["package_manager"],
        vulnerable_version=item["vulnerable_version"],
        severity=item.get("severity"),
        source=item["source"],
        created_at=item.get("created_at"),
        modified_at=item.get("modified_at"),
    )


def _check_severity(advisory: Advisory) -> bool:
    severity = advisory.severity
    if severity is None and advisory.source != PATCH_SRC:
        return True
    if severity is None:
        return False
    severity_elems = severity.split("/")
    if len(severity_elems) != 9:
        return False
    cvss, ver = severity_elems[0].split(":")
    if (
        cvss != "CVSS"
        or not ver.replace(".", "", 1).isdigit()
        or not ver.startswith("3")
    ):
        return False
    for index, (key, values) in enumerate(CVSS_BASE_METRICS.items(), 1):
        metric, value = severity_elems[index].split(":")
        if metric != key or value not in values:
            return False
    return True


def _check_versions(versions: str) -> bool:
    if not versions:
        return False
    version_list = versions.split(" || ")
    for version_range in version_list:
        range_ver = version_range.split()
        if not all(ver.startswith(VALID_RANGES) for ver in range_ver):
            return False
    semver_match("1.0", versions, True)
    return True


def format_advisory(
    advisory: Advisory,
    is_update: bool = False,
    checked: bool = False,
) -> Advisory:
    severity = advisory.severity
    if not checked:
        if not _check_versions(advisory.vulnerable_version):
            raise InvalidVulnerableVersion()
        if not _check_severity(advisory):
            if advisory.source != PATCH_SRC:
                severity = None
            else:
                raise InvalidSeverity()

    current_date = str(datetime.now())

    return Advisory(
        associated_advisory=advisory.associated_advisory,
        package_name=advisory.package_name.lower(),
        package_manager=advisory.package_manager.lower(),
        vulnerable_version=advisory.vulnerable_version.lower(),
        severity=severity,
        source=advisory.source,
        created_at=current_date if (not is_update) else advisory.created_at,
        modified_at=current_date if is_update else None,
    )


def format_advisory_to_item(advisory: Advisory) -> Item:
    return {
        "associated_advisory": advisory.associated_advisory,
        "package_name": advisory.package_name,
        "package_manager": advisory.package_manager,
        "vulnerable_version": advisory.vulnerable_version,
        "severity": advisory.severity,
        "source": advisory.source,
        "created_at": advisory.created_at,
        "modified_at": advisory.modified_at,
    }


def print_exc(
    exc: _SingleMessageException,
    action: str,
    advisory: Advisory,
    attr: str = "",
) -> None:
    log_blocking(
        "warning",
        (
            "Advisory PLATFORM#%s#PACKAGE#%s SOURCE#%s#ADVISORY#%s "
            "wasn't %s. %s%s"
        ),
        advisory.package_manager,
        advisory.package_name,
        advisory.source,
        advisory.associated_advisory,
        action,
        exc.new(),
        attr,
    )
