from aioextensions import (
    collect,
)
from collections.abc import (
    Callable,
    Iterable,
)
from custom_exceptions import (
    InvalidAcceptanceDays,
    InvalidAcceptanceSeverity,
    InvalidNumberAcceptances,
    InvalidParameter,
    InvalidPath,
    InvalidPort,
    InvalidSource,
    InvalidStream,
    InvalidVulnCommitHash,
    InvalidVulnerabilityAlreadyExists,
    InvalidVulnSpecific,
    InvalidVulnWhere,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model.constants import (
    DEFAULT_MAX_SEVERITY,
    DEFAULT_MIN_SEVERITY,
)
from db_model.enums import (
    Source,
)
from db_model.groups.types import (
    Group,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityTreatment,
)
from decimal import (
    Decimal,
)
import functools
from newutils import (
    datetime as datetime_utils,
)
from newutils.validations import (
    check_exp,
    get_attr_value,
)
from organizations.utils import (
    get_organization,
)
import re
from string import (
    hexdigits,
)
from typing import (
    Any,
)
from urllib.parse import (
    urlparse,
)
from vulnerabilities.domain.utils import (
    get_hash,
    get_hash_from_typed,
    get_path_from_integrates_vulnerability,
)


async def get_policy_max_acceptance_days(
    *, loaders: Dataloaders, group_name: str
) -> int | None:
    group: Group = await loaders.group.load(group_name)
    if group.policies:
        return group.policies.max_acceptance_days

    organization = await get_organization(loaders, group.organization_id)

    return organization.policies.max_acceptance_days


async def get_policy_max_number_acceptances(
    *, loaders: Dataloaders, group_name: str
) -> int | None:
    group: Group = await loaders.group.load(group_name)
    if group.policies:
        return group.policies.max_number_acceptances

    organization = await get_organization(loaders, group.organization_id)

    return organization.policies.max_number_acceptances


async def get_policy_max_acceptance_severity(
    *, loaders: Dataloaders, group_name: str
) -> Decimal:
    group: Group = await loaders.group.load(group_name)
    if group.policies:
        return (
            group.policies.max_acceptance_severity
            if group.policies.max_acceptance_severity is not None
            else DEFAULT_MAX_SEVERITY
        )

    organization = await get_organization(loaders, group.organization_id)

    return (
        organization.policies.max_acceptance_severity
        if organization.policies.max_acceptance_severity is not None
        else DEFAULT_MAX_SEVERITY
    )


async def get_policy_min_acceptance_severity(
    *, loaders: Dataloaders, group_name: str
) -> Decimal:
    group: Group = await loaders.group.load(group_name)
    if group.policies:
        return group.policies.min_acceptance_severity or DEFAULT_MIN_SEVERITY

    organization = await get_organization(loaders, group.organization_id)

    return (
        organization.policies.min_acceptance_severity or DEFAULT_MIN_SEVERITY
    )


async def validate_acceptance_days(
    loaders: Dataloaders,
    accepted_until: datetime,
    group_name: str,
) -> None:
    """
    Checks if acceptance date complies with group and organization policies.
    """
    today = datetime_utils.get_utc_now()
    acceptance_days = Decimal((accepted_until - today).days)
    max_acceptance_days = await get_policy_max_acceptance_days(
        loaders=loaders, group_name=group_name
    )
    if (
        max_acceptance_days is not None
        and acceptance_days > max_acceptance_days
    ) or acceptance_days < 0:
        raise InvalidAcceptanceDays(
            "Chosen date is either in the past or exceeds "
            "the maximum number of days allowed by the defined policy"
        )


async def validate_acceptance_severity(
    loaders: Dataloaders,
    group_name: str,
    severity: Decimal,
) -> None:
    """
    Checks if the severity to be temporarily accepted is inside
    the range set by the defined policy.
    """
    min_value = await get_policy_min_acceptance_severity(
        loaders=loaders, group_name=group_name
    )
    max_value = await get_policy_max_acceptance_severity(
        loaders=loaders, group_name=group_name
    )
    if not min_value <= severity <= max_value:
        raise InvalidAcceptanceSeverity(str(severity))


async def validate_number_acceptances(
    loaders: Dataloaders,
    group_name: str,
    historic_treatment: Iterable[VulnerabilityTreatment],
) -> None:
    """
    Check that a vulnerability to temporarily accept does not exceed the
    maximum number of acceptances the organization set.
    """
    max_acceptances = await get_policy_max_number_acceptances(
        loaders=loaders, group_name=group_name
    )
    current_acceptances: int = sum(
        1
        for item in historic_treatment
        if item.status == VulnerabilityTreatmentStatus.ACCEPTED
    )
    if (
        max_acceptances is not None
        and current_acceptances + 1 > max_acceptances
    ):
        raise InvalidNumberAcceptances(
            str(current_acceptances) if current_acceptances else "-"
        )


async def validate_accepted_treatment_change(
    *,
    loaders: Dataloaders,
    accepted_until: datetime,
    finding_severity: Decimal,
    group_name: str,
    historic_treatment: Iterable[VulnerabilityTreatment],
) -> None:
    await collect(
        [
            validate_acceptance_days(loaders, accepted_until, group_name),
            validate_acceptance_severity(
                loaders, group_name, finding_severity
            ),
            validate_number_acceptances(
                loaders, group_name, historic_treatment
            ),
        ]
    )


def validate_lines_specific(specific: str) -> None:
    if not specific.isdigit():
        raise InvalidVulnSpecific.new()


def validate_ports_specific(specific: str) -> None:
    if not specific.isdigit():
        raise InvalidVulnSpecific.new()
    if not 0 <= int(specific) <= 65535:
        raise InvalidPort(expr=f'"values": "{specific}"')


def validate_uniqueness(
    *,
    finding_vulns_data: tuple[Vulnerability, ...],
    vulnerability_where: str,
    vulnerability_specific: str,
    vulnerability_type: VulnerabilityType,
    vulnerability_id: str,
) -> None:
    current_vuln = next(
        (item for item in finding_vulns_data if item.id == vulnerability_id),
        None,
    )
    if not current_vuln:
        return
    new_vuln_hash: int = get_hash(
        specific=vulnerability_specific,
        type_=vulnerability_type.value,
        where=get_path_from_integrates_vulnerability(
            vulnerability_where, vulnerability_type
        )[1]
        if current_vuln.type == VulnerabilityType.INPUTS
        else vulnerability_where,
        root_id=current_vuln.root_id,
    )
    for vuln in finding_vulns_data:
        vuln_hash = get_hash_from_typed(vuln)
        if vuln_hash == new_vuln_hash:
            raise InvalidVulnerabilityAlreadyExists.new()


def validate_commit_hash(vuln_commit: str) -> None:
    if len(vuln_commit) != 40 or not set(hexdigits).issuperset(
        set(vuln_commit)
    ):
        raise InvalidVulnCommitHash.new()


def validate_stream(
    where: str,
    stream: str,
    index: int,
    vuln_type: str,
) -> bool:
    url_parsed = urlparse(where)
    if (len(url_parsed.path) == 0 or url_parsed.path == "/") and not (
        stream.lower().startswith("home,")
        or stream.lower().startswith("query,")
    ):
        raise InvalidStream(vuln_type, f"{index}")
    return True


def validate_where(where: str) -> None:
    if not re.match("^[^=/]+.+$", where):
        raise InvalidVulnWhere.new()


def validate_where_deco(where_field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            where = get_attr_value(
                field=where_field, kwargs=kwargs, obj_type=str
            )
            check_exp(where, r"^[^=/]+.+$", InvalidVulnWhere.new())
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_path(path: str) -> None:
    # Use Unix-like paths
    if path.find("\\") >= 0:
        invalid_path = path.replace("\\", "\\\\")
        raise InvalidPath(expr=f'"values": "{invalid_path}"')


def validate_path_deco(path_field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            path = get_attr_value(
                field=path_field, kwargs=kwargs, obj_type=Source
            )
            if path.find("\\") >= 0:
                invalid_path = path.replace("\\", "\\\\")
                raise InvalidPath(expr=f'"values": "{invalid_path}"')
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_source(source: Source) -> None:
    if source not in {
        Source.ANALYST,
        Source.CUSTOMER,
        Source.DETERMINISTIC,
        Source.ESCAPE,
        Source.MACHINE,
    }:
        raise InvalidSource()


def validate_source_deco(source_field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            source = get_attr_value(
                field=source_field, kwargs=kwargs, obj_type=Source
            )
            if source and source not in {
                Source.ANALYST,
                Source.CUSTOMER,
                Source.DETERMINISTIC,
                Source.ESCAPE,
                Source.MACHINE,
            }:
                raise InvalidSource()
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_updated_commit_deco(
    vulnerability_type_field: str, commit_field: str
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            vulnerability_type = get_attr_value(
                field=vulnerability_type_field, kwargs=kwargs, obj_type=str
            )
            commit = get_attr_value(
                field=commit_field, kwargs=kwargs, obj_type=str
            )
            if commit:
                if vulnerability_type is not VulnerabilityType.LINES:
                    raise InvalidParameter("commit")
                validate_commit_hash(commit)
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_updated_specific_deco(
    vulnerability_type_field: str, specific_field: str
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            vulnerability_type = get_attr_value(
                field=vulnerability_type_field,
                kwargs=kwargs,
                obj_type=str,
            )
            specific = get_attr_value(
                field=specific_field,
                kwargs=kwargs,
                obj_type=str,
            )
            if specific and vulnerability_type is VulnerabilityType.LINES:
                validate_lines_specific(specific)
            if specific and vulnerability_type is VulnerabilityType.PORTS:
                validate_ports_specific(specific)
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_updated_where_deco(
    vulnerability_type_field: str, where_field: str
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            vulnerability_type = get_attr_value(
                field=vulnerability_type_field,
                kwargs=kwargs,
                obj_type=str,
            )
            where = get_attr_value(
                field=where_field,
                kwargs=kwargs,
                obj_type=str,
            )
            if where:
                if vulnerability_type is VulnerabilityType.LINES:
                    validate_path(where)
                validate_where(where)
            return func(*args, **kwargs)

        return decorated

    return wrapper
