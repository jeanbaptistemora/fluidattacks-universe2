from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.bar_chart.exposure_trends_by_categories import (
    get_categories,
    get_data_vulnerabilities,
    GroupInformation,
)
from charts.utils import (
    CsvData,
    get_portfolios_groups,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
)
from custom_exceptions import (
    UnsanitizedInputFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decimal import (
    Decimal,
)
from newutils.validations import (
    validate_sanitized_csv_input,
)
from organizations.domain import (
    get_all_active_group_names,
)
from statistics import (
    mean,
)
from typing import (
    Counter,
    NamedTuple,
)

CATEGORIES: dict[str, str] = get_categories()


class Benchmarking(NamedTuple):
    value: Counter[str]
    subject: str


def format_csv_data(
    *, document: dict, header: str, alternative: str
) -> CsvData:
    columns: list[list[str]] = [
        document["data"][0]["name"],
        document["data"][1]["name"],
    ]
    categories: list[str] = [
        value["axis"] for value in document["data"][0]["axes"]
    ]
    rows: list[list[str]] = []
    for index, category in enumerate(categories):
        row_values: list[str] = [
            str(data["axes"][index]["value"]) for data in document["data"]
        ]
        try:
            validate_sanitized_csv_input(str(category))
            rows.append([str(category), *row_values])
        except UnsanitizedInputFound:
            rows.append(["", ""])

    return CsvData(
        headers=[header, *[f"{column} {alternative}" for column in columns]],
        rows=rows,
    )


def get_finding_value(
    findings_cvssf: dict[str, Decimal],
    vulnerabilities: tuple[Vulnerability, ...],
) -> Decimal:
    return Decimal(
        sum(
            findings_cvssf[str(vulnerability.finding_id)]
            if vulnerability.state.status == VulnerabilityStateStatus.OPEN
            else Decimal("0.0")
            for vulnerability in vulnerabilities
        )
    ).quantize(Decimal("0.1"))


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    *,
    group: str,
    loaders: Dataloaders,
) -> Benchmarking:
    data: GroupInformation = await get_data_vulnerabilities(
        group=group,
        loaders=loaders,
    )

    vulnerabilities_by_categories = [
        {
            f"{data.categories[finding.id]}": get_finding_value(
                data.cvssf, vulnerabilities
            )
        }
        for finding, vulnerabilities in zip(
            data.findings, data.finding_vulnerabilities
        )
    ]

    return Benchmarking(
        subject=group,
        value=sum(
            [Counter(source) for source in vulnerabilities_by_categories],
            Counter(),
        ),
    )


@alru_cache(maxsize=None, typed=True)
async def get_data_many_groups(
    *,
    subject: str,
    groups: tuple[str, ...],
    loaders: Dataloaders,
) -> Benchmarking:
    groups_data: tuple[Benchmarking, ...] = await collect(
        tuple(
            get_data_one_group(group=group, loaders=loaders)
            for group in groups
        ),
        workers=32,
    )

    return Benchmarking(
        subject=subject,
        value=sum([group.value for group in groups_data], Counter()),
    )


def get_average_entities(
    *, entities: tuple[Benchmarking, ...], categories: list[str]
) -> Counter[str]:
    if entities:

        return Counter(
            {
                category: Decimal(
                    mean([subject.value[category] for subject in entities])
                ).quantize(Decimal("0.1"))
                for category in categories
            }
        )

    return Counter()


def get_subjects(
    *,
    all_subjects: tuple[Benchmarking, ...],
    subject: str,
) -> tuple[Benchmarking, ...]:
    return tuple(
        entity for entity in all_subjects if subject != entity.subject
    )


def format_data(
    *,
    data_name: str,
    data: Benchmarking,
    average_name: str,
    average: Counter[str],
    categories: list[str],
) -> dict:

    return dict(
        legend="Vulnerabilities categories",
        data=[
            dict(
                name=data_name,
                axes=[
                    {
                        "axis": category,
                        "value": Decimal(data.value[category]).quantize(
                            Decimal("0.1")
                        ),
                    }
                    for category in categories
                ],
            ),
            dict(
                name=average_name,
                axes=[
                    {
                        "axis": category,
                        "value": Decimal(average[category]).quantize(
                            Decimal("0.1")
                        ),
                    }
                    for category in categories
                ],
            ),
        ],
    )


async def generate() -> None:  # pylint: disable=too-many-locals
    loaders: Dataloaders = get_new_context()
    organizations: list[tuple[str, tuple[str, ...]]] = []
    portfolios: list[tuple[str, tuple[str, ...]]] = []
    header: str = "Categories"
    alternative: str = "exposure"
    unique_categories: list[str] = list(sorted(set(CATEGORIES.values())))
    group_names: list[str] = list(
        sorted(
            await get_all_active_group_names(loaders),
            reverse=True,
        )
    )

    async for org_id, org_name, org_groups in (
        iterate_organizations_and_groups()
    ):
        organizations.append((org_id, org_groups))
        for portfolio, p_groups in await get_portfolios_groups(org_name):
            portfolios.append(
                (f"{org_id}PORTFOLIO#{portfolio}", tuple(p_groups))
            )

    all_groups_data: tuple[Benchmarking, ...] = await collect(
        tuple(
            get_data_one_group(
                group=group_name,
                loaders=loaders,
            )
            for group_name in group_names
        ),
        workers=24,
    )

    all_organizations_data: tuple[Benchmarking, ...] = await collect(
        tuple(
            get_data_many_groups(
                groups=organization[1],
                loaders=loaders,
                subject=organization[0],
            )
            for organization in organizations
        ),
        workers=24,
    )

    async for group in iterate_groups():
        document = format_data(
            data_name="My group",
            data=await get_data_one_group(
                group=group,
                loaders=loaders,
            ),
            categories=unique_categories,
            average_name="Average groups",
            average=get_average_entities(
                entities=get_subjects(
                    all_subjects=all_groups_data,
                    subject=group,
                ),
                categories=unique_categories,
            ),
        )
        json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(
                document=document, header=header, alternative=alternative
            ),
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        document = format_data(
            data_name="My organization",
            data=await get_data_many_groups(
                subject=org_id,
                groups=org_groups,
                loaders=loaders,
            ),
            average_name="Average organizations",
            average=get_average_entities(
                entities=get_subjects(
                    all_subjects=all_organizations_data,
                    subject=org_id,
                ),
                categories=unique_categories,
            ),
            categories=unique_categories,
        )
        json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(
                document=document, header=header, alternative=alternative
            ),
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, group_names in await get_portfolios_groups(org_name):
            document = format_data(
                data_name="My portfolio",
                data=await get_data_many_groups(
                    subject=f"{org_id}PORTFOLIO#{portfolio}",
                    groups=tuple(group_names),
                    loaders=loaders,
                ),
                average_name="Average organizations",
                average=get_average_entities(
                    entities=get_subjects(
                        all_subjects=all_organizations_data,
                        subject=f"{org_id}PORTFOLIO#{portfolio}",
                    ),
                    categories=unique_categories,
                ),
                categories=unique_categories,
            )
            json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(
                    document=document,
                    header=header,
                    alternative=alternative,
                ),
            )


if __name__ == "__main__":
    run(generate())
