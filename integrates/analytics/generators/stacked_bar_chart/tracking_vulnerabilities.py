# Standard library
from typing import (
    Dict,
    List,
    Union,
)

# Third party libraries
from aioextensions import run
from backend.api.dataloaders.finding_vulns import FindingVulnsLoader
from backend.domain.finding import (
    get_findings_by_group,
    get_tracking_vulnerabilities,
)

# Local libraries
from analytics import (
    utils,
)
from analytics.colors import (
    RISK,
)


async def generate_one(finding_id: str) -> List[Dict[str, Union[int, str]]]:
    vulns = await FindingVulnsLoader().load(finding_id)
    tracking = await get_tracking_vulnerabilities(vulns)
    return tracking[-12:]


def format_document(tracking: List[Dict[str, Union[int, str]]]) -> dict:
    return dict(
        data=dict(
            x='date',
            columns=[
                ['date'] + [cycle.get('date') for cycle in tracking],
                ['Open'] + [cycle.get('open') for cycle in tracking],
                ['Closed'] + [cycle.get('closed') for cycle in tracking],
                ['% Effectiveness'] + [
                    cycle.get('effectiveness') for cycle in tracking
                ],
            ],
            axes={
                'Open': 'y',
                'Closed': 'y2',
                '% Effectiveness': 'y2',
            },
            order=None,
            colors={
                'Open': RISK.more_agressive,
                'Closed': RISK.more_passive,
                '% Effectiveness': RISK.neutral,
            },
            types={
                'Open': 'line',
                'Closed': 'bar',
                '% Effectiveness': 'bar',
            },
        ),
        bar=dict(
            width=0,
        ),
        axis=dict(
            x=dict(
                tick=dict(
                    centered=True,
                    multiline=False,
                    rotate=12,
                ),
                type='category',
            ),
            y2=dict(
                show=False,
            ),
        ),
        legend=dict(
            position='bottom',
            hide=['Closed', '% Effectiveness']
        ),
        grid=dict(
            x=dict(
                show=True,
            ),
            y=dict(
                show=True,
            ),
        ),
        point=dict(
            focus=dict(
                expand=dict(
                    enabled=True,
                ),
            ),
            r=5,
        ),
    )


async def generate_all():
    async for group in utils.iterate_groups():
        for finding in await get_findings_by_group(group):
            utils.json_dump(
                document=format_document(
                    tracking=await generate_one(str(finding['id'])),
                ),
                entity='finding',
                subject=str(finding['id']),
            )


if __name__ == '__main__':
    run(generate_all())
