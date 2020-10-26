# Standard library
from datetime import datetime, timedelta
from itertools import chain
from typing import (
    List,
    Tuple
)

# Third party libraries
from aioextensions import run
from backend.api.dataloaders.project import (
    ProjectLoader as GroupLoader,
)
from backend.api.dataloaders.finding_vulns import FindingVulnsLoader
from backend.typing import (
    Vulnerability as VulnerabilityType
)

# Local libraries
from analytics import (
    utils,
)


def had_state_by_then(
    last_day: datetime,
    state: str,
    vuln: VulnerabilityType
) -> bool:
    historic_state = reversed(vuln['historic_state'])
    last_state: dict = next(
        filter(
            lambda item:
            datetime.strptime(
                item['date'],
                '%Y-%m-%d %H:%M:%S'
            ) <= last_day,
            historic_state
        ),
        dict()
    )

    return last_state.get('state') == state


def get_totals_by_week(
    vulns: List[VulnerabilityType],
    last_day: datetime
) -> Tuple[int, int]:
    open_vulns = len(tuple(
        filter(
            lambda vuln: had_state_by_then(
                last_day=last_day,
                state='open',
                vuln=vuln,
            ),
            vulns
        )
    ))
    closed_vulns = len(tuple(
        filter(
            lambda vuln: had_state_by_then(
                last_day=last_day,
                state='closed',
                vuln=vuln,
            ),
            vulns
        )
    ))

    return open_vulns, closed_vulns


async def generate_one(groups: List[str]):
    groups_data = list(filter(
        lambda group: group['attrs'].get('project_status') == 'ACTIVE',
        await GroupLoader().load_many(groups)
    ))

    current_rolling_week = datetime.now()
    previous_rolling_week = current_rolling_week - timedelta(days=7)

    total_previous_open: int = 0
    total_previous_closed: int = 0
    total_current_open: int = 0
    total_current_closed: int = 0

    for group in groups_data:
        vulns = list(filter(
            lambda vuln: vuln['current_approval_status'] != 'PENDING',
            chain(*await FindingVulnsLoader().load_many(group['findings']))
        ))

        open_last_week, closed_last_week = get_totals_by_week(
            vulns,
            previous_rolling_week,
        )
        total_previous_open += open_last_week
        total_previous_closed += closed_last_week

        currently_open, currently_closed = get_totals_by_week(
            vulns,
            current_rolling_week,
        )
        total_current_open += currently_open
        total_current_closed += currently_closed

    return {
        'current': {
            'closed': total_current_closed,
            'open': total_current_open,
        },
        'previous': {
            'closed': total_previous_closed,
            'open': total_previous_open,
        },
        'totalGroups': len(groups_data)
    }


async def generate_all():
    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=await generate_one(org_groups),
            entity='organization',
            subject=org_id,
        )


if __name__ == '__main__':
    run(generate_all())
