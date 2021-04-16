"""
This migration is related to the removed approval flow for vulnerabilities.
It takes those PENDING vulns and reject them as before.
Executed: 2020-08-31 12:20:00-05:00
"""

import os
from time import time
from typing import (
    Dict,
    List,
)

import django
from aioextensions import (
    collect,
    run,
)

from findings import domain as findings_domain
from groups import domain as groups_domain
from vulnerabilities import (
    dal as vulns_dal,
    domain as vulns_domain,
)


django.setup()
STAGE: str = os.environ['STAGE']


async def reject_vulnerabilities(group: str) -> None:
    findings = await findings_domain.list_findings([group])
    for finding_id in findings[0]:
        vulns = await vulns_domain.list_vulnerabilities_async([finding_id])
        for vuln in vulns:
            vuln_uuid = vuln.get('UUID')
            historic_state = vuln.get('historic_state', [{}])
            last_state = historic_state[-1]
            if 'approval_status' in last_state and \
                last_state.get('approval_status') == 'PENDING':
                if not await reject_vulnerability(
                    finding_id,
                    historic_state,
                    vuln_uuid
                ):
                    print(
                        f'Some error happened while rejecting vuln {vuln_uuid}'
                        f' of finding {finding_id} in group {group}'
                    )
                else:
                    print(
                        f'Success rejecting vuln {vuln_uuid}'
                        f' of finding {finding_id} in group {group}'
                    )


async def reject_vulnerability(
        finding_id: str,
        historic_state: List[Dict[str, str]],
        vuln_id: str) -> bool:
    """ old reject_vulnerability function"""
    historic_state.pop()
    response = False
    if historic_state:
        response = await vulns_dal.update(
            finding_id,
            vuln_id,
            {'historic_state': historic_state}
        )
    else:
        response = await vulns_dal.delete(vuln_id, finding_id)
    return response


async def main() -> None:
    groups = await groups_domain.get_active_projects()
    await collect(
        reject_vulnerabilities(group)
        for group in groups
    )


if __name__ == '__main__':
    run(main())
