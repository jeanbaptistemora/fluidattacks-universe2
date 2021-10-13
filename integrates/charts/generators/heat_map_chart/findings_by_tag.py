from aioextensions import (
    collect,
    run,
)
from charts import (
    utils,
)
from custom_types import (
    Finding,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.types import (
    Finding as FindingNew,
)
from itertools import (
    chain,
)
from typing import (
    Counter,
    Dict,
    List,
    NamedTuple,
    Set,
    Tuple,
)

FindingsTags = NamedTuple(
    "FindingsTags",
    [
        ("counter", Counter[str]),
        ("counter_finding", Counter[str]),
        ("findings", List[str]),
        ("tags", Set[str]),
    ],
)


async def get_data_finding(
    finding_title: str, vulnerabilities: List[Dict[str, Finding]]
) -> FindingsTags:
    title = finding_title.split(".")[0]
    tags: List[str] = list(
        filter(
            None,
            chain.from_iterable(
                map(lambda x: x["tag"].split(", "), vulnerabilities)
            ),
        )
    )

    return FindingsTags(
        counter=Counter(tags),
        counter_finding=Counter([f"{title}/{tag}" for tag in tags]),
        findings=[title] if tags else [],
        tags=set(tags),
    )


async def get_data(group: str) -> FindingsTags:
    context = get_new_context()
    group_findings_loader = context.group_findings
    group_findings: Tuple[FindingNew, ...] = await group_findings_loader.load(
        group.lower()
    )
    finding_ids = [finding.id for finding in group_findings]
    findings = [finding.title for finding in group_findings]

    vulnerabilities = await context.finding_vulns_nzr.load_many(finding_ids)

    findings_data = await collect(
        [
            get_data_finding(finding_title, vulns)
            for finding_title, vulns in zip(findings, vulnerabilities)
        ]
    )
    all_tags = [finding_data.tags for finding_data in findings_data]

    return FindingsTags(
        counter=sum(
            [finding_data.counter for finding_data in findings_data], Counter()
        ),
        counter_finding=sum(
            [finding_data.counter_finding for finding_data in findings_data],
            Counter(),
        ),
        findings=[
            finding_data.findings[0]
            for finding_data in findings_data
            if finding_data.findings
        ],
        tags=set.union(*all_tags) if all_tags else set(),
    )


def format_data(data: FindingsTags) -> dict:
    max_value: List[Tuple[str, int]] = data.counter_finding.most_common(1)
    tags: Set[str] = {tag for tag, _ in data.counter.most_common()[:10]}
    findings: Set[str] = {
        finding
        for finding in data.findings
        for tag in tags
        if data.counter_finding[f"{finding}/{tag}"] > 0
    }

    return dict(
        x=findings,
        grid_values=[
            {
                "value": data.counter_finding[f"{finding}/{tag}"],
                "x": finding,
                "y": tag,
            }
            for finding in findings
            for tag in tags
        ],
        y=tags,
        max_value=max_value[0][1] if max_value else 1,
        tick_rotate=utils.TICK_ROTATION,
    )


async def generate_all() -> None:
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(data=await get_data(group)),
            entity="group",
            subject=group,
        )


if __name__ == "__main__":
    run(generate_all())
