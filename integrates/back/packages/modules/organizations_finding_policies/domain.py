# Standard libraries
from itertools import chain
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)
from uuid import uuid4

# Third-party libraries
from aioextensions import (
    collect,
    schedule,
)

# Local libraries
from backend.api import Dataloaders
from backend.typing import (
    Finding,
)
from custom_exceptions import (
    FindingNamePolicyNotFound,
    InvalidFindingNamePolicy,
    PolicyAlreadyHandled,
    RepeatedFindingNamePolicy,
)
from dynamodb.types import (
    OrgFindingPolicyItem,
    OrgFindingPolicyMetadata,
    OrgFindingPolicyState,
)
from newutils import (
    datetime as datetime_utils,
    findings as findings_utils,
    vulnerabilities as vulns_utils
)
from redis_cluster.operations import redis_del_by_deps
from vulnerabilities import dal as vulns_dal
from .dal import (
    add_org_finding_policy,
    get_org_finding_policies,
    get_org_finding_policy,
    update_finding_policy_status,
)


async def get_finding_policy(
    *,
    org_name: str,
    finding_policy_id: str
) -> OrgFindingPolicyItem:
    finding_policy = await get_org_finding_policy(
        org_name=org_name,
        finding_policy_id=finding_policy_id
    )
    if finding_policy:
        return finding_policy

    raise FindingNamePolicyNotFound()


async def get_finding_policies(
    *,
    org_name: str
) -> Tuple[OrgFindingPolicyItem, ...]:
    return await get_org_finding_policies(org_name=org_name)


def validate_finding_name(name: str) -> None:
    if not findings_utils.is_valid_finding_title(name):
        raise InvalidFindingNamePolicy()


async def get_finding_policy_by_name(
    *,
    org_name: str,
    finding_name: str
) -> Optional[OrgFindingPolicyItem]:
    return next(
        (
            fin_policy
            for fin_policy in await get_finding_policies(org_name=org_name)
            if fin_policy.metadata.name.split('.')[0].lower() == finding_name
        ),
        None
    )


async def add_finding_policy(
    *,
    finding_name: str,
    org_name: str,
    user_email: str,
) -> None:
    validate_finding_name(finding_name)
    finding_policy = await get_finding_policy_by_name(
        org_name=org_name,
        finding_name=finding_name.split('.')[0].lower(),
    )
    if finding_policy:
        raise RepeatedFindingNamePolicy()

    new_finding_policy = OrgFindingPolicyItem(
        org_name=org_name,
        id=str(uuid4()),
        metadata=OrgFindingPolicyMetadata(
            name=finding_name
        ),
        state=OrgFindingPolicyState(
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            status='SUBMITTED'
        )
    )
    await add_org_finding_policy(finding_policy=new_finding_policy)


async def handle_finding_policy_acceptation(
    *,
    finding_policy_id: str,
    loaders: Dataloaders,
    org_name: str,
    status: str,
    groups: List[str],
    user_email: str
) -> None:
    finding_policy = await get_finding_policy(
        org_name=org_name,
        finding_policy_id=finding_policy_id
    )
    if finding_policy.state.status != 'SUBMITTED':
        raise PolicyAlreadyHandled()

    await update_finding_policy_status(
        org_name=org_name,
        finding_policy_id=finding_policy_id,
        status=OrgFindingPolicyState(
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            status=status
        )
    )

    if status == 'APPROVED':
        finding_name: str = finding_policy.metadata.name.split('.')[0].lower()
        schedule(
            update_treatment_in_org_groups(
                finding_name=finding_name,
                loaders=loaders,
                groups=groups,
                status=status,
                user_email=user_email
            )
        )


async def deactivate_finding_policy(
    *,
    finding_policy_id: str,
    loaders: Dataloaders,
    org_name: str,
    groups: List[str],
    user_email: str
) -> None:
    finding_policy = await get_finding_policy(
        org_name=org_name,
        finding_policy_id=finding_policy_id
    )
    if finding_policy.state.status != 'APPROVED':
        raise PolicyAlreadyHandled()

    status: str = 'INACTIVE'
    await update_finding_policy_status(
        org_name=org_name,
        finding_policy_id=finding_policy_id,
        status=OrgFindingPolicyState(
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            status=status
        )
    )

    finding_name: str = finding_policy.metadata.name.split('.')[0].lower()
    schedule(
        update_treatment_in_org_groups(
            finding_name=finding_name,
            loaders=loaders,
            groups=groups,
            status=status,
            user_email=user_email
        )
    )


async def update_treatment_in_org_groups(
    *,
    finding_name: str,
    loaders: Dataloaders,
    groups: List[str],
    status: str,
    user_email: str
) -> None:
    group_drafts = await loaders.group_drafts.load_many(groups)
    group_findings = await loaders.group_findings.load_many(groups)
    findings: List[Dict[str, Finding]] = list(
        chain.from_iterable(filter(None, group_drafts + group_findings))
    )

    findings_ids: List[str] = [
        finding['id'] for finding in findings
        if finding['title'].split('.')[0].lower() == finding_name
    ]
    if not findings_ids:
        return
    vulns = await loaders.finding_vulns_nzr.load_many_chained(findings_ids)

    await _apply_finding_policy(
        findings_ids=findings_ids,
        vulns=vulns,
        status=status,
        user_email=user_email
    )


async def _apply_finding_policy(
    findings_ids: List[str],
    vulns: List[Dict[str, Finding]],
    status: str,
    user_email: str,
) -> None:
    current_day: str = datetime_utils.get_now_as_str()
    if status == 'APPROVED':
        return await _add_accepted_treatment(
            current_day=current_day,
            findings_ids=findings_ids,
            vulns=vulns,
            user_email=user_email,
        )

    if status == 'INACTIVE':
        return await _add_new_treatment(
            current_day=current_day,
            findings_ids=findings_ids,
            vulns=vulns,
            user_email=user_email,
        )


async def _add_accepted_treatment(
    *,
    current_day: str,
    findings_ids: List[str],
    vulns: List[Dict[str, Finding]],
    user_email: str
) -> None:
    vulns_to_update = [
        vuln for vuln in vulns
        if vuln['historic_treatment'][-1] != 'ACCEPTED_UNDEFINED'
        and vuln['current_state'] == 'open'
    ]
    new_treatments = vulns_utils.get_treatment_from_org_finding_policy(
        current_day=current_day,
        user_email=user_email
    )
    await _update_treatment_in_org_groups(
        findings_ids=findings_ids,
        new_treatments=new_treatments,
        vulns_to_update=vulns_to_update,
    )


async def _add_new_treatment(
    *,
    current_day: str,
    findings_ids: List[str],
    vulns: List[Dict[str, Finding]],
    user_email: str
) -> None:
    new_treatments = [{
        'date': current_day,
        'treatment': 'NEW',
        'user': user_email,
    }]
    await _update_treatment_in_org_groups(
        findings_ids=findings_ids,
        new_treatments=new_treatments,
        vulns_to_update=vulns,
    )


async def _update_treatment_in_org_groups(
    *,
    findings_ids: List[str],
    new_treatments: List[Dict[str, str]],
    vulns_to_update: List[Dict[str, Finding]],
) -> None:
    historics_treatments = [
        [*vuln['historic_treatment'], *new_treatments]
        for vuln in vulns_to_update
    ]

    await collect([
        vulns_dal.update(
            vuln['finding_id'],
            vuln['UUID'],
            {'historic_treatment': historic_treatment}
        )
        for vuln, historic_treatment in zip(
            vulns_to_update,
            historics_treatments
        )
    ])

    await collect([
        redis_del_by_deps(
            'update_treatment_vulnerability',
            finding_id=finding_id
        )
        for finding_id in findings_ids
    ])
