#/usr/bin/env python3
#-.- coding: utf-8 -.-
"""
This migration aims to verify vulnerabilities with requested
re-attack that was closed manually (using yaml) so currently
can't be verified

Execution Time: 2020-08-21 14:00:51 UTC-5
Finalization Time: 2020-08-21 14:05:10 UTC-5
"""
from collections import (
    defaultdict,
)
from datetime import datetime
from time import time
import os
from typing import (
    Awaitable,
    Dict,
    List,
    Union,
    cast,
)

from aioextensions import (
    collect,
    run,
)
import django
from django.conf import settings
from more_itertools import chunked
import pytz

from backend.dal import (
    comment as comment_dal,
    finding as finding_dal,
    vulnerability as vuln_dal,
)
from backend.domain import (
    project as group_domain,
    user as user_domain,
    vulnerability as vuln_domain,
)
from backend.typing import (
    Comment as CommentType,
)
django.setup()
STAGE: str = os.environ['STAGE']


async def should_verify_closed_vulnerabilities(group: str) -> None:
    findings = await group_domain.list_findings([group])
    for finding in findings[0]:
        closed_vulns: Dict[str, List[str]] = defaultdict(list)
        vulns = await vuln_domain.list_vulnerabilities_async([finding])
        for vuln in vulns:
            current_status = vuln_domain.get_last_approved_status(vuln)
            current_verification = vuln.get(
                'historic_verification', [{}]
            )[-1].get('status', '')
            should_verify = (
                current_status == 'closed' and
                current_verification == 'REQUESTED'
            )
            last_state = vuln_domain.get_last_approved_state(vuln)
            user_email = last_state.get('analyst', '').replace('api-', '')
            if should_verify:
                closed_vulns[user_email].append(vuln.get('UUID'))

        for email, list_vulns in closed_vulns.items():
            if STAGE == 'apply':
                name_attrs = cast(
                    Dict[str, str],
                    await user_domain.get_attributes(
                        email, ['first_name', 'last_name']
                    )
                )
                await collect(
                    verify_closed_vulnerabilities(
                        finding_id=finding,
                        user_email=email,
                        user_fullname=' '.join(list(name_attrs.values())),
                        closed_vulns=list_vuln,
                        group=group,
                    )
                    for list_vuln in chunked(list_vulns, 10)
                )


async def verify_closed_vulnerabilities(
    finding_id: str,
    user_email: str,
    user_fullname: str,
    closed_vulns: List[str],
    group: str,
) -> None:
    coroutines: List[Awaitable[bool]] = []
    finding = await finding_dal.get_finding(finding_id)
    vulnerabilities = await vuln_domain.get_by_ids(closed_vulns)
    tzn = pytz.timezone(settings.TIME_ZONE)
    today = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
    comment_id = int(round(time() * 1000))

    historic_verification = cast(
        List[Dict[str, Union[str, int, List[str]]]],
        finding.get('historic_verification', [])
    )
    historic_verification.append({
        'date': today,
        'user': user_email,
        'status': 'VERIFIED',
        'comment': comment_id,
        'vulns': closed_vulns
    })
    coroutines.append(
        finding_dal.update(
            finding_id, {'historic_verification': historic_verification}
        )
    )
    comment_data: CommentType = {
        'comment_type': 'verification',
        'content': 'The vulnerability was verified by closing it',
        'created': today,
        'email': user_email,
        'finding_id': int(finding_id),
        'fullname': user_fullname,
        'modified': today,
        'parent': 0,
    }
    coroutines.append(comment_dal.create(comment_id, comment_data))
    coroutines.extend(map(vuln_dal.verify_vulnerability, vulnerabilities))
    await collect(coroutines)


async def main() -> None:
    groups = await group_domain.get_active_projects()
    await collect(
        should_verify_closed_vulnerabilities(group)
        for group in groups
    )


if __name__ == '__main__':
    run(main())
