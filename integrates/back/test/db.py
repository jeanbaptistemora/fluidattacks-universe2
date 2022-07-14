from aioextensions import (
    collect,
)
from authz import (
    policy as authz_policy,
)
from batch.dal import (
    put_action_to_dynamodb,
)
from comments import (
    dal as dal_comment,
)
from dataloaders import (
    get_new_context,
)
from db_model import (
    credentials as creds_model,
    events as events_model,
    findings as findings_model,
    groups as groups_model,
    organizations as orgs_model,
    roots as roots_model,
    toe_inputs as toe_inputs_model,
    toe_lines as toe_lines_model,
    vulnerabilities as vulns_model,
)
from db_model.credentials.types import (
    Credentials,
)
from db_model.events.types import (
    Event,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
    FindingUnreliableIndicators,
)
from db_model.groups.types import (
    Group,
)
from db_model.roots.types import (
    GitRoot,
    Root,
)
from db_model.stakeholders.types import (
    NotificationsPreferences,
    StakeholderMetadataToUpdate,
)
from db_model.toe_inputs.types import (
    ToeInput,
)
from db_model.toe_lines.types import (
    ToeLines,
)
from db_model.types import (
    PoliciesToUpdate,
)
from dynamodb.types import (
    OrgFindingPolicyItem,
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
from stakeholders import (
    dal as dal_stakeholders,
)
from typing import (
    Any,
    Awaitable,
    Dict,
    List,
    Tuple,
)


async def populate_stakeholders(data: List[Any]) -> bool:
    await collect(
        [
            dal_stakeholders.add_typed(
                stakeholder=item["stakeholder"],
            )
            for item in data
        ]
    )
    await collect(
        [
            dal_stakeholders.update_metadata(
                stakeholder_email=user["stakeholder"].email,
                metadata=StakeholderMetadataToUpdate(
                    notifications_preferences=NotificationsPreferences(
                        email=[
                            "ACCESS_GRANTED",
                            "AGENT_TOKEN",
                            "CHARTS_REPORT",
                            "DAILY_DIGEST",
                            "EVENT_REPORT",
                            "FILE_UPDATE",
                            "GROUP_INFORMATION",
                            "GROUP_REPORT",
                            "NEW_COMMENT",
                            "NEW_DRAFT",
                            "PORTFOLIO_UPDATE",
                            "REMEDIATE_FINDING",
                            "REMINDER_NOTIFICATION",
                            "ROOT_UPDATE",
                            "SERVICE_UPDATE",
                            "UNSUBSCRIPTION_ALERT",
                            "UPDATED_TREATMENT",
                            "VULNERABILITY_ASSIGNED",
                            "VULNERABILITY_REPORT",
                        ]
                    )
                ),
            )
            for user in data
        ]
    )
    return True


async def populate_organization_users(data: list[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    for org in data:
        for user in org["users"]:
            coroutines.append(
                dal_organizations.add_user(
                    f'ORG#{org["id"]}',
                    user,
                )
            )
    return all(await collect(coroutines))


async def populate_organizations(data: list[Any]) -> bool:
    await collect(
        orgs_model.add(
            organization=item["organization"],
        )
        for item in data
    )
    return True


async def _populate_group_policies(data: dict[str, Any]) -> None:
    group: Group = data["group"]
    if data.get("policies"):
        await groups_model.update_policies(
            group_name=group.name,
            modified_by=group.policies.modified_by,
            modified_date=group.policies.modified_date,
            organization_id=group.organization_id,
            policies=PoliciesToUpdate(
                max_acceptance_days=group.policies.max_acceptance_days,
                max_acceptance_severity=group.policies.max_acceptance_severity,
                max_number_acceptances=group.policies.max_number_acceptances,
            ),
        )


async def _populate_group_unreliable_indicators(data: Dict[str, Any]) -> None:
    group: Group = data["group"]
    if data.get("unreliable_indicators"):
        await groups_model.update_unreliable_indicators(
            group_name=group.name,
            indicators=data["unreliable_indicators"],
        )


async def _populate_group_historic_state(data: Dict[str, Any]) -> None:
    group: Group = data["group"]
    historic = data.get("historic_state", [])
    for state in historic:
        await groups_model.update_state(
            group_name=group.name,
            organization_id=group.organization_id,
            state=state,
        )


async def populate_groups(data: List[Dict[str, Any]]) -> bool:
    await collect(
        groups_model.add(
            group=item["group"],
        )
        for item in data
    )
    await collect([_populate_group_historic_state(item) for item in data])
    await collect(
        [_populate_group_unreliable_indicators(item) for item in data]
    )
    await collect(
        tuple(_populate_group_policies(item) for item in data),
        workers=16,
    )
    return True


async def _populate_finding_unreliable_indicator(data: Dict[str, Any]) -> None:
    finding = data["finding"]
    if data.get("unreliable_indicator"):
        await findings_model.update_unreliable_indicators(
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
        await findings_model.update_state(
            current_value=previous,
            group_name=finding.group_name,
            finding_id=finding.id,
            state=current,
        )
        if current.status == FindingStateStatus.APPROVED:
            await findings_model.update_me_draft_index(
                finding_id=finding.id,
                group_name=finding.group_name,
                user_email="",
            )


async def _populate_finding_historic_verification(
    data: Dict[str, Any]
) -> None:
    # Update the finding verification sequentially is important to
    # not generate a race condition
    finding: Finding = data["finding"]
    historic = (finding.verification, *data["historic_verification"])
    for previous, current in zip(historic, historic[1:]):
        await findings_model.update_verification(
            current_value=previous,
            group_name=finding.group_name,
            finding_id=finding.id,
            verification=current,
        )


async def _populate_root_historic_state(data: Dict[str, Any]) -> None:
    root: Root = data["root"]
    historic = (root.state, *data["historic_state"])
    for previous, current in zip(historic, historic[1:]):
        await roots_model.update_root_state(
            current_value=previous,
            group_name=root.group_name,
            root_id=root.id,
            state=current,
        )


async def populate_findings(data: List[Dict[str, Any]]) -> bool:
    await collect(
        [findings_model.add(finding=item["finding"]) for item in data]
    )
    await collect([_populate_finding_historic_state(item) for item in data])
    await collect(
        [_populate_finding_unreliable_indicator(item) for item in data]
    )
    await collect(
        [_populate_finding_historic_verification(item) for item in data]
    )
    await collect(
        [
            findings_model.remove(
                group_name=item["finding"].group_name,
                finding_id=item["finding"].id,
            )
            for item in data
            if item["historic_state"]
            and item["historic_state"][-1].status == FindingStateStatus.DELETED
        ]
    )
    return True


async def populate_vulnerabilities(data: List[Dict[str, Any]]) -> bool:
    await collect(
        [
            vulns_model.add(vulnerability=vulnerability["vulnerability"])
            for vulnerability in data
        ]
    )
    vuln_ids = [item["vulnerability"].id for item in data]
    loaders = get_new_context()
    current_vulnerabilities = await loaders.vulnerability.load_many(vuln_ids)
    await collect(
        [
            vulns_model.update_historic(
                current_value=current_value,
                historic=vulnerability["historic_state"],
            )
            for current_value, vulnerability in zip(
                current_vulnerabilities, data
            )
            if "historic_state" in vulnerability
        ]
    )
    loaders = get_new_context()
    current_vulnerabilities = await loaders.vulnerability.load_many(vuln_ids)
    await collect(
        [
            vulns_model.update_historic(
                current_value=current_value,
                historic=vulnerability["historic_treatment"],
            )
            for current_value, vulnerability in zip(
                current_vulnerabilities, data
            )
            if "historic_treatment" in vulnerability
        ]
    )
    loaders = get_new_context()
    current_vulnerabilities = await loaders.vulnerability.load_many(vuln_ids)
    await collect(
        [
            vulns_model.update_historic(
                current_value=current_value,
                historic=vulnerability["historic_verification"],
            )
            for current_value, vulnerability in zip(
                current_vulnerabilities, data
            )
            if "historic_verification" in vulnerability
        ]
    )
    loaders = get_new_context()
    current_vulnerabilities = await loaders.vulnerability.load_many(vuln_ids)
    await collect(
        [
            vulns_model.update_historic(
                current_value=current_value,
                historic=vulnerability["historic_zero_risk"],
            )
            for current_value, vulnerability in zip(
                current_vulnerabilities, data
            )
            if "historic_zero_risk" in vulnerability
        ]
    )

    return True


async def populate_roots(data: List[Dict[str, Any]]) -> bool:
    await collect(tuple(roots_model.add(root=item["root"]) for item in data))
    await collect([_populate_root_historic_state(item) for item in data])
    await collect(
        [
            roots_model.add_git_environment_url(item["root"].id, url)
            for item in data
            if isinstance(item["root"], GitRoot)
            for url in item["root"].state.git_environment_urls
        ]
    )

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


async def _populate_event_historic_state(data: Dict[str, Any]) -> None:
    event: Event = data["event"]
    historic = data.get("historic_state", [])
    current_value = event
    for state in historic:
        await events_model.update_state(
            current_value=current_value,
            group_name=event.group_name,
            state=state,
        )
        current_value = event._replace(state=state)


async def populate_events(data: List[Any]) -> bool:
    await collect(
        events_model.add(
            event=item["event"],
        )
        for item in data
    )
    await collect([_populate_event_historic_state(item) for item in data])
    return True


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


async def populate_credentials(data: Tuple[Credentials, ...]) -> bool:
    await collect(
        (creds_model.add(credential=credential)) for credential in data
    )
    return True


async def populate_actions(data: Tuple[Dict[str, Any], ...]) -> bool:
    await collect((put_action_to_dynamodb(**action)) for action in data)
    return True


async def populate(data: Dict[str, Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    functions: Dict[str, Any] = globals()
    for name, dataset in data.items():
        coroutines.append(functions[f"populate_{name}"](dataset))
    return all(await collect(coroutines))
