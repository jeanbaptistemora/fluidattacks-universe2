from aioextensions import (
    collect,
)
import authz
from batch.dal import (
    put_action_to_dynamodb,
)
from dataloaders import (
    get_new_context,
)
from db_model import (
    credentials as creds_model,
    enrollment as enrollment_model,
    events as events_model,
    findings as findings_model,
    group_access as group_access_model,
    groups as groups_model,
    organization_access as org_access_model,
    organizations as orgs_model,
    roots as roots_model,
    stakeholders as stakeholders_model,
    toe_inputs as toe_inputs_model,
    toe_lines as toe_lines_model,
    vulnerabilities as vulns_model,
)
from db_model.credentials.types import (
    Credentials,
)
from db_model.enrollment.types import (
    Enrollment,
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
from db_model.group_access.types import (
    GroupAccessMetadataToUpdate,
)
from db_model.groups.types import (
    Group,
)
from db_model.organization_access.types import (
    OrganizationAccess,
    OrganizationAccessMetadataToUpdate,
)
from db_model.roots.types import (
    GitRoot,
    Root,
)
from db_model.stakeholders.types import (
    NotificationsPreferences,
    Stakeholder,
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
from event_comments.dal import (
    create_typed,
)
from finding_comments import (
    dal as dal_comment,
)
from forces import (
    dal as dal_forces,
)
from group_comments import (
    dal as dal_group_comments,
)
from newutils.datetime import (
    get_from_str,
)
from organizations_finding_policies import (
    dal as dal_policies,
)
from typing import (
    Any,
    Awaitable,
)


async def populate_stakeholders(data: list[Stakeholder]) -> bool:
    await collect(
        stakeholders_model.update_metadata(
            email=item.email,
            metadata=StakeholderMetadataToUpdate(
                access_token=item.access_token,
                first_name=item.first_name,
                is_concurrent_session=item.is_concurrent_session,
                is_registered=item.is_registered,
                last_login_date=item.last_login_date,
                last_name=item.last_name,
                legal_remember=item.legal_remember,
                notifications_preferences=NotificationsPreferences(
                    email=[
                        "ACCESS_GRANTED",
                        "AGENT_TOKEN",
                        "CHARTS_REPORT",
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
                ),
                phone=item.phone,
                push_tokens=item.push_tokens,
                registration_date=item.registration_date,
                role=item.role,
                tours=item.tours,
            ),
        )
        for item in data
    )
    return True


async def populate_organization_access(data: list[OrganizationAccess]) -> bool:
    await collect(
        org_access_model.update_metadata(
            email=item.email,
            organization_id=item.organization_id,
            metadata=OrganizationAccessMetadataToUpdate(),
        )
        for item in data
    )
    return True


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


async def _populate_group_unreliable_indicators(data: dict[str, Any]) -> None:
    group: Group = data["group"]
    if data.get("unreliable_indicators"):
        await groups_model.update_unreliable_indicators(
            group_name=group.name,
            indicators=data["unreliable_indicators"],
        )


async def _populate_group_historic_state(data: dict[str, Any]) -> None:
    group: Group = data["group"]
    historic = data.get("historic_state", [])
    for state in historic:
        await groups_model.update_state(
            group_name=group.name,
            organization_id=group.organization_id,
            state=state,
        )


async def populate_groups(data: list[dict[str, Any]]) -> bool:
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


async def _populate_finding_unreliable_indicator(data: dict[str, Any]) -> None:
    finding = data["finding"]
    if data.get("unreliable_indicator"):
        await findings_model.update_unreliable_indicators(
            current_value=FindingUnreliableIndicators(),
            group_name=finding.group_name,
            finding_id=finding.id,
            indicators=data["unreliable_indicator"],
        )


async def _populate_finding_historic_state(data: dict[str, Any]) -> None:
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
    data: dict[str, Any]
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


async def _populate_root_historic_state(data: dict[str, Any]) -> None:
    root: Root = data["root"]
    historic = (root.state, *data["historic_state"])
    for previous, current in zip(historic, historic[1:]):
        await roots_model.update_root_state(
            current_value=previous,
            group_name=root.group_name,
            root_id=root.id,
            state=current,
        )


async def populate_findings(data: list[dict[str, Any]]) -> bool:
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


async def populate_vulnerabilities(data: list[dict[str, Any]]) -> bool:
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


async def populate_roots(data: list[dict[str, Any]]) -> bool:
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


async def populate_consultings(data: list[Any]) -> bool:
    await collect(
        dal_group_comments.add_comment_typed(
            comment_data=item["group_comment"]
        )
        for item in data
    )
    return True


async def _populate_event_historic_state(data: dict[str, Any]) -> None:
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


async def populate_events(data: list[Any]) -> bool:
    await collect(
        events_model.add(
            event=item["event"],
        )
        for item in data
    )
    await collect([_populate_event_historic_state(item) for item in data])
    return True


async def populate_enrollments(data: tuple[Enrollment, ...]) -> bool:
    await collect(
        enrollment_model.add(enrollment=enrollment) for enrollment in data
    )
    return True


async def populate_event_comments(data: list[Any]) -> bool:
    await collect(
        create_typed(
            comment_attributes=item["event_comment"],
        )
        for item in data
    )
    return True


async def populate_finding_comments(data: list[Any]) -> bool:
    await collect(
        dal_comment.create_typed(
            comment_attributes=item["finding_comment"],
        )
        for item in data
    )
    return True


async def populate_policies(data: list[Any]) -> bool:
    coroutines: list[Awaitable[bool]] = []
    coroutines.extend(
        [
            authz.grant_user_level_role(
                email=policy["subject"],
                role=policy["role"],
            )
            for policy in data
            if policy["level"] == "user"
        ]
    )
    coroutines.extend(
        [
            authz.grant_organization_level_role(
                email=policy["subject"],
                organization_id=policy["object"],
                role=policy["role"],
            )
            for policy in data
            if policy["level"] == "organization"
        ]
    )
    coroutines.extend(
        [
            authz.grant_group_level_role(
                email=policy["subject"],
                group_name=policy["object"],
                role=policy["role"],
            )
            for policy in data
            if policy["level"] == "group"
        ]
    )
    success = all(await collect(coroutines))

    if success:
        await collect(
            [
                group_access_model.update_metadata(
                    email=policy["subject"],
                    group_name=policy["object"],
                    metadata=GroupAccessMetadataToUpdate(
                        has_access=True,
                    ),
                )
                for policy in data
                if policy["level"] == "group"
            ]
        )

    return success


async def populate_organization_finding_policies(
    data: tuple[OrgFindingPolicyItem, ...]
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


async def populate_executions(data: list[Any]) -> bool:
    coroutines: list[Awaitable[bool]] = []
    for execution in data:
        execution["date"] = get_from_str(
            execution["date"], date_format="%Y-%m-%dT%H:%M:%SZ", zone="UTC"
        )
    coroutines.extend(
        [dal_forces.add_execution(**execution) for execution in data]
    )
    return all(await collect(coroutines))


async def populate_toe_inputs(data: tuple[ToeInput, ...]) -> bool:
    await collect(
        [toe_inputs_model.add(toe_input=toe_input) for toe_input in data]
    )
    return True


async def populate_toe_lines(data: tuple[ToeLines, ...]) -> bool:
    await collect(
        [toe_lines_model.add(toe_lines=toe_lines) for toe_lines in data]
    )
    return True


async def populate_credentials(data: tuple[Credentials, ...]) -> bool:
    await collect(
        (creds_model.add(credential=credential)) for credential in data
    )
    return True


async def populate_actions(data: tuple[dict[str, Any], ...]) -> bool:
    await collect((put_action_to_dynamodb(**action)) for action in data)
    return True


async def populate(data: dict[str, Any]) -> bool:
    coroutines: list[Awaitable[bool]] = []
    functions: dict[str, Any] = globals()
    for name, dataset in data.items():
        coroutines.append(functions[f"populate_{name}"](dataset))
    return all(await collect(coroutines))
