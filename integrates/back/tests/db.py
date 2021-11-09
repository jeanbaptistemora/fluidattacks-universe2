from aioextensions import (
    collect,
)
from authz import (
    policy as authz_policy,
)
from comments import (
    dal as dal_comment,
)
from db_model import (
    findings,
    roots as roots_model,
    services_toe_lines as services_toe_lines_model,
    toe_inputs as toe_inputs_model,
    toe_lines as toe_lines_model,
    vulnerabilities,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
    FindingUnreliableIndicators,
)
from db_model.roots.types import (
    RootItem,
)
from db_model.services_toe_lines.types import (
    ServicesToeLines,
)
from db_model.toe_inputs.types import (
    ToeInput,
)
from db_model.toe_lines.types import (
    ToeLines,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decimal import (
    Decimal,
)
from dynamodb.types import (
    OrgFindingPolicyItem,
)
from events import (
    dal as dal_event,
)
from forces import (
    dal as dal_forces,
)
from group_access import (
    dal as dal_group_access,
)
from group_comments import (
    dal as dal_group_comments,
)
from groups import (
    dal as dal_groups,
)
import json
from names import (
    dal as dal_names,
)
from newutils.datetime import (
    get_from_str,
)
from newutils.utils import (
    get_key_or_fallback,
)
from organizations import (
    dal as dal_organizations,
)
from organizations_finding_policies import (
    dal as dal_policies,
)
from typing import (
    Any,
    Awaitable,
    Dict,
    List,
    Tuple,
)
from users import (
    dal as dal_users,
)
from vulnerabilities import (
    dal as dal_vulns,
)


async def populate_users(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    coroutines.extend(
        [
            dal_users.create(
                user["email"],
                user,
            )
            for user in data
        ]
    )
    return all(await collect(coroutines))


async def populate_names(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    coroutines.extend(
        [
            dal_names.create(
                name["name"],
                name["entity"],
            )
            for name in data
        ]
    )
    return all(await collect(coroutines))


async def populate_orgs(data: List[Any]) -> bool:
    success: bool = False
    coroutines: List[Awaitable[bool]] = []
    for org in data:
        coroutines.append(
            dal_organizations.create(
                org["name"],
                org["id"],
            )
        )
        for user in org["users"]:
            coroutines.append(
                dal_organizations.add_user(
                    f'ORG#{org["id"]}',
                    user,
                )
            )
        for group in org["groups"]:
            coroutines.append(
                dal_organizations.add_group(
                    f'ORG#{org["id"]}',
                    group,
                )
            )
    success = all(await collect(coroutines))
    coroutines = []
    coroutines.extend(
        [
            dal_organizations.update(
                f'ORG#{org["id"]}',
                org["name"],
                org["policy"],
            )
            for org in data
            if org["policy"]
        ]
    )
    success = success and all(await collect(coroutines))
    return success


async def populate_groups(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    data_parsed: List[Any] = json.loads(json.dumps(data), parse_float=Decimal)
    coroutines.extend(
        [
            dal_groups.add(
                group,
            )
            for group in data_parsed
        ]
    )
    return all(await collect(coroutines))


async def _populate_finding_unreliable_indicator(data: Dict[str, Any]) -> None:
    finding = data["finding"]
    if data.get("unreliable_indicator"):
        await findings.update_unreliable_indicators(
            current_value=FindingUnreliableIndicators(),
            group_name=finding.group_name,
            finding_id=finding.id,
            indicators=data["unreliable_indicator"],
        )


async def _populate_finding_historic_state(data: Dict[str, Any]) -> None:
    # Update the finding state sequentially is important to
    # not generate a race condition
    finding: Finding = data["finding"]
    historic = (finding.state, *data["historic_state"])
    for previous, current in zip(historic, historic[1:]):
        await findings.update_state(
            current_value=previous,
            group_name=finding.group_name,
            finding_id=finding.id,
            state=current,
        )


async def _populate_finding_historic_verification(
    data: Dict[str, Any]
) -> None:
    # Update the finding verification sequentially is important to
    # not generate a race condition
    finding: Finding = data["finding"]
    historic = (finding.verification, *data["historic_verification"])
    for previous, current in zip(historic, historic[1:]):
        await findings.update_verification(
            current_value=previous,
            group_name=finding.group_name,
            finding_id=finding.id,
            verification=current,
        )


async def populate_findings(data: List[Dict[str, Any]]) -> bool:
    await collect([findings.add(finding=item["finding"]) for item in data])
    await collect([_populate_finding_historic_state(item) for item in data])
    await collect(
        [_populate_finding_unreliable_indicator(item) for item in data]
    )
    await collect(
        [_populate_finding_historic_verification(item) for item in data]
    )
    await collect(
        [
            findings.remove(
                group_name=item["finding"].group_name,
                finding_id=item["finding"].id,
            )
            for item in data
            if item["historic_state"]
            and item["historic_state"][-1].status == FindingStateStatus.DELETED
        ]
    )
    return True


async def _populate_vuln_historic_state(data: Dict[str, Any]) -> None:
    if "historic_state" in data:
        vuln: Vulnerability = data["vulnerability"]
        for state in data["historic_state"]:
            await vulnerabilities.update_state(
                current_value=vuln.state,
                finding_id=vuln.finding_id,
                state=state,
                vulnerability_id=vuln.id,
            )


async def _populate_vuln_historic_treatment(data: Dict[str, Any]) -> None:
    if "historic_treatment" in data:
        vuln: Vulnerability = data["vulnerability"]
        for treatment in data["historic_treatment"]:
            await vulnerabilities.update_treatment(
                current_value=vuln.treatment,
                finding_id=vuln.finding_id,
                treatment=treatment,
                vulnerability_id=vuln.id,
            )


async def _populate_vuln_historic_verification(data: Dict[str, Any]) -> None:
    if "historic_verification" in data:
        vuln: Vulnerability = data["vulnerability"]
        for verification in data["historic_verification"]:
            await vulnerabilities.update_verification(
                current_value=vuln.verification,
                finding_id=vuln.finding_id,
                verification=verification,
                vulnerability_id=vuln.id,
            )


async def _populate_vuln_historic_zero_risk(data: Dict[str, Any]) -> None:
    if "historic_zero_risk" in data:
        vuln: Vulnerability = data["vulnerability"]
        for zero_risk in data["historic_zero_risk"]:
            await vulnerabilities.update_zero_risk(
                current_value=vuln.zero_risk,
                finding_id=vuln.finding_id,
                zero_risk=zero_risk,
                vulnerability_id=vuln.id,
            )


async def populate_vulnerabilities_new(data: List[Dict[str, Any]]) -> bool:
    await collect(
        [
            vulnerabilities.add(vulnerability=item["vulnerability"])
            for item in data
        ]
    )
    await collect([_populate_vuln_historic_state(item) for item in data])
    await collect([_populate_vuln_historic_treatment(item) for item in data])
    await collect(
        [_populate_vuln_historic_verification(item) for item in data]
    )
    await collect([_populate_vuln_historic_zero_risk(item) for item in data])
    return True


async def populate_vulnerabilities(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    coroutines.extend(
        [
            dal_vulns.create(
                vulnerability,
            )
            for vulnerability in data
        ]
    )
    coroutines.extend(
        [
            dal_vulns.update(
                vulnerability["finding_id"],
                vulnerability["UUID"],
                {"historic_zero_risk": vulnerability["historic_zero_risk"]},
            )
            for vulnerability in data
            if vulnerability.get("historic_zero_risk")
        ]
    )
    return all(await collect(coroutines))


async def populate_roots(data: Tuple[RootItem, ...]) -> bool:
    await collect(tuple(roots_model.add(root=root) for root in data))

    return True


async def populate_consultings(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    coroutines.extend(
        [
            dal_group_comments.add_comment(
                get_key_or_fallback(consulting),
                consulting["email"],
                consulting,
            )
            for consulting in data
        ]
    )
    return all(await collect(coroutines))


async def populate_events(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    coroutines.extend(
        [
            dal_event.create(
                event["event_id"],
                get_key_or_fallback(event),
                event,
            )
            for event in data
        ]
    )
    return all(await collect(coroutines))


async def populate_comments(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    coroutines.extend(
        [
            dal_comment.create(
                comment["comment_id"],
                comment,
                comment["finding_id"],
            )
            for comment in data
        ]
    )
    return all(await collect(coroutines))


async def populate_policies(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    coroutines.extend(
        [
            authz_policy.put_subject_policy(
                authz_policy.SubjectPolicy(
                    level=policy["level"],
                    subject=policy["subject"],
                    object=policy["object"],
                    role=policy["role"],
                ),
            )
            for policy in data
        ]
    )
    coroutines.extend(
        [
            dal_group_access.update(
                policy["subject"],
                policy["object"],
                {"has_access": True},
            )
            for policy in data
            if policy["level"] == "group"
        ]
    )
    return all(await collect(coroutines))


async def populate_organization_finding_policies(
    data: Tuple[OrgFindingPolicyItem, ...]
) -> bool:
    await collect(
        [
            dal_policies.add_organization_finding_policy(
                finding_policy=finding_policy
            )
            for finding_policy in data
        ]
    )

    return True


async def populate_executions(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    for execution in data:
        execution["date"] = get_from_str(
            execution["date"], date_format="%Y-%m-%dT%H:%M:%SZ", zone="UTC"
        )
    coroutines.extend(
        [dal_forces.add_execution(**execution) for execution in data]
    )
    return all(await collect(coroutines))


async def populate_services_toe_lines(
    data: Tuple[ServicesToeLines, ...]
) -> bool:
    await collect(
        [
            services_toe_lines_model.add(services_toe_lines=services_toe_lines)
            for services_toe_lines in data
        ]
    )
    return True


async def populate_toe_inputs(data: Tuple[ToeInput, ...]) -> bool:
    await collect(
        [toe_inputs_model.add(toe_input=toe_input) for toe_input in data]
    )
    return True


async def populate_toe_lines(data: Tuple[ToeLines, ...]) -> bool:
    await collect(
        [toe_lines_model.add(toe_lines=toe_lines) for toe_lines in data]
    )
    return True


async def populate(data: Dict[str, Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    functions: Dict[str, Any] = globals()
    for name, dataset in data.items():
        coroutines.append(functions[f"populate_{name}"](dataset))
    return all(await collect(coroutines))
