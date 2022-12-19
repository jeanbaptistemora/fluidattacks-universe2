import asyncio
import contextlib
import csv
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.enums import (
    GroupSubscriptionType,
)
from db_model.portfolios.types import (
    Portfolio,
)
from decimal import (
    Decimal,
    ROUND_CEILING,
    ROUND_FLOOR,
)
import functools
import json
import math
from newutils.encodings import (
    safe_encode,
)
from organizations import (
    domain as orgs_domain,
)
import os
from typing import (
    Any,
    AsyncIterator,
    Callable,
    NamedTuple,
    Optional,
    Type,
)


class PortfoliosGroups(NamedTuple):
    portfolio: str
    groups: tuple[str, ...]


class CsvData(NamedTuple):
    headers: list[str]
    rows: list[list[str]]


TICK_ROTATION = 20  # rotation displayed for group name and vulnerability type
MAX_WITH_DECIMALS = Decimal("10.0")


def get_result_path(name: str) -> str:
    return os.path.join(os.environ["RESULTS_DIR"], name)


async def get_portfolios_groups(org_name: str) -> list[PortfoliosGroups]:
    loaders: Dataloaders = get_new_context()
    portfolios: tuple[
        Portfolio, ...
    ] = await loaders.organization_portfolios.load(org_name)

    return [
        PortfoliosGroups(
            portfolio=data.id,
            groups=tuple(data.groups),
        )
        for data in portfolios
    ]


async def iterate_groups() -> AsyncIterator[str]:
    loaders: Dataloaders = get_new_context()
    active_groups_names = await orgs_domain.get_all_active_group_names(loaders)
    for group_name in sorted(active_groups_names, reverse=True):
        log_info(f"Working on group: {group_name}")
        # Exception: WF(AsyncIterator is subtype of iterator)
        yield group_name  # NOSONAR


async def iterate_organizations_and_groups() -> AsyncIterator[
    tuple[str, str, tuple[str, ...]],
]:
    """Yield (org_id, org_name, org_groups) non-concurrently generated."""
    loaders: Dataloaders = get_new_context()
    active_groups = sorted(await orgs_domain.get_all_active_groups(loaders))
    group_names: set[str] = {
        group.name
        for group in active_groups
        if group.state.type == GroupSubscriptionType.CONTINUOUS
    }
    async for org_id, org_name, org_groups in (
        orgs_domain.iterate_organizations_and_groups(loaders)
    ):
        log_info(f"Working on org: {org_id} ({org_name}) {org_groups}")
        # Exception: WF(AsyncIterator is subtype of iterator)
        yield (  # NOSONAR
            org_id,
            org_name,
            tuple(group_names.intersection(org_groups)),
        )


def json_dump(
    *,
    document: object,
    entity: str,
    subject: str,
    csv_document: Optional[CsvData] = None,
) -> None:
    for result_path in map(
        get_result_path,
        [
            f"{entity}:{safe_encode(subject.lower())}",
        ],
    ):
        with open(f"{result_path}.json", "w", encoding="utf-8") as json_file:
            json.dump(document, json_file, default=json_encoder, indent=2)

        if csv_document:
            with open(f"{result_path}.csv", "w", encoding="utf-8") as csv_file:
                writer = csv.writer(
                    csv_file,
                    delimiter=",",
                    quotechar='"',
                    quoting=csv.QUOTE_MINIMAL,
                )
                writer.writerow(csv_document.headers)
                writer.writerows(csv_document.rows)


# Using Any because this is a generic-input function
def json_encoder(obj: Any) -> Any:
    obj_type: type = type(obj)

    if obj_type == set:
        casted_obj: Any = [json_encoder(value) for value in obj]
    elif obj_type == Decimal:
        casted_obj = float(obj)
    else:
        casted_obj = obj

    return casted_obj


# Using Any because this is a generic-input function
def log_info(*args: Any, **kwargs: Any) -> None:
    print("[INFO]", *args, **kwargs)


# Using Any because this is a generic-input decorator
def retry_on_exceptions(
    *,
    default_value: Any,
    exceptions: tuple[Type[Exception], ...],
    retry_times: int,
) -> Callable[..., Any]:
    def decorator(function: Callable[..., Any]) -> Callable[..., Any]:

        if asyncio.iscoroutinefunction(function):

            @functools.wraps(function)
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                for _ in range(retry_times):
                    with contextlib.suppress(*exceptions):
                        return await function(*args, **kwargs)

                return default_value

        else:

            @functools.wraps(function)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                for _ in range(retry_times):
                    with contextlib.suppress(*exceptions):
                        return function(*args, **kwargs)

                return default_value

        return wrapper

    return decorator


def get_cvssf(severity: Decimal) -> Decimal:
    return Decimal(pow(Decimal("4.0"), severity - Decimal("4.0"))).quantize(
        Decimal("0.001")
    )


def get_subject_days(days: Optional[int]) -> str:
    if days:
        return f"_{days}"
    return ""


def format_cvssf(cvssf: Decimal) -> Decimal:
    if abs(cvssf) >= MAX_WITH_DECIMALS:
        if cvssf > Decimal("0.0"):
            return cvssf.to_integral_exact(rounding=ROUND_CEILING)

        return cvssf.to_integral_exact(rounding=ROUND_FLOOR)

    return cvssf.quantize(Decimal("0.1"))


def format_cvssf_log(cvssf: Decimal) -> Decimal:
    if cvssf <= Decimal("0.0"):
        return cvssf.quantize(Decimal("0.1"))

    if cvssf >= MAX_WITH_DECIMALS:
        return Decimal(
            math.log2(cvssf.to_integral_exact(rounding=ROUND_CEILING))
        )

    return Decimal(math.log2(cvssf))
