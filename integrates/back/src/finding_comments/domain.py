# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    schedule,
)
import authz
from custom_exceptions import (
    RootNotFound,
)
from dataloaders import (
    Dataloaders,
)
from db_model import (
    finding_comments as finding_comments_model,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingComment,
)
from db_model.findings.types import (
    Finding,
    FindingVerification,
)
from db_model.roots.types import (
    Root,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decimal import (
    Decimal,
)
from group_access.domain import (
    get_stakeholders_subscribed_to_consult,
)
from itertools import (
    filterfalse,
)
from mailer import (
    findings as findings_mail,
)
from typing import (
    Any,
    Dict,
    Optional,
    TypedDict,
)


class VulnsProperties(TypedDict):
    remaining_exposure: int
    severity_level: str
    severity_score: Decimal
    vulns_props: Dict[str, Dict[str, Dict[str, Any]]]


async def get_vuln_nickname(
    loaders: Dataloaders,
    vuln: Vulnerability,
) -> str:
    try:
        root: Root = await loaders.root.load((vuln.group_name, vuln.root_id))
        if vuln.type == "LINES":
            return f"  {root.state.nickname}/{vuln.state.where}"
    except RootNotFound:
        pass
    return vuln.state.where


async def _fill_vuln_info(
    loaders: Dataloaders,
    comment: FindingComment,
    vulns_ids: set[str],
    vulns: tuple[Vulnerability, ...],
) -> FindingComment:
    """Adds the «Regarding vulnerabilities...» header to comments answering a
    solicited reattack."""
    selected_vulns = [
        f"  - {await get_vuln_nickname(loaders, vuln)}"
        for vuln in vulns
        if vuln.id in vulns_ids
    ]
    selected_vulns = list(set(selected_vulns))
    wheres = "\n".join(selected_vulns)
    # Avoid needless repetition of the header if the comment is answering more
    # than one reattack
    if not comment.content.startswith(
        f"Regarding vulnerabilities: \n{wheres}"
    ):
        comment = comment._replace(
            content=f"Regarding vulnerabilities: \n{wheres}\n\n"
            + comment.content
        )
    return comment


def _is_scope_comment(comment: FindingComment) -> bool:
    return str(comment.content).strip() not in {"#external", "#internal"}


async def send_finding_consult_mail(
    loaders: Dataloaders,
    comment_data: FindingComment,
) -> None:
    if _is_scope_comment(comment_data):
        finding_id = comment_data.finding_id
        finding: Finding = await loaders.finding.load(finding_id)
        group_name: str = finding.group_name
        is_finding_released = bool(finding.approval)
        finding_title = finding.title
        user_email = comment_data.email
        await findings_mail.send_mail_comment(
            loaders=loaders,
            comment_data=comment_data,
            user_mail=user_email,
            finding_id=finding_id,
            finding_title=finding_title,
            recipients=await get_stakeholders_subscribed_to_consult(
                loaders=loaders,
                group_name=group_name,
                comment_type=comment_data.comment_type.value.lower(),
                is_finding_released=is_finding_released,
            ),
            group_name=group_name,
            is_finding_released=is_finding_released,
        )


async def add(
    loaders: Dataloaders,
    comment_data: FindingComment,
    notify: bool = False,
    closed_properties: Optional[VulnsProperties] = None,
) -> None:
    await finding_comments_model.add(finding_comment=comment_data)
    if notify:
        schedule(send_finding_consult_mail(loaders, comment_data))
    if closed_properties is not None:
        finding: Finding = await loaders.finding.load(comment_data.finding_id)
        schedule(
            findings_mail.send_mail_vulnerability_report(
                loaders=loaders,
                group_name=finding.group_name,
                finding_title=finding.title,
                finding_id=comment_data.finding_id,
                vulnerabilities_properties=closed_properties["vulns_props"],
                responsible=finding.state.modified_by,
                remaining_exposure=closed_properties["remaining_exposure"],
                severity_score=closed_properties["severity_score"],
                severity_level=closed_properties["severity_level"],
                is_closed=True,
            )
        )


async def remove(comment_id: str, finding_id: str) -> None:
    await finding_comments_model.remove(
        comment_id=comment_id, finding_id=finding_id
    )


async def get_comments(
    loaders: Dataloaders,
    group_name: str,
    finding_id: str,
    user_email: str,
) -> tuple[FindingComment, ...]:
    comments = await loaders.finding_comments.load(
        (CommentType.COMMENT, finding_id)
    )
    historic_verification: tuple[
        FindingVerification, ...
    ] = await loaders.finding_historic_verification.load(finding_id)
    verified = tuple(
        verification
        for verification in historic_verification
        if verification.vulnerability_ids
    )
    if bool(verified):
        verification_comment_ids: set[str] = {
            verification.comment_id for verification in verified
        }
        vulns: tuple[
            Vulnerability, ...
        ] = await loaders.finding_vulnerabilities.load(finding_id)

        reattack_comments, non_reattack_comments = filter_reattack_comments(
            comments, verification_comment_ids
        )
        # Loop to add the «Regarding vulnerabilities...» header to comments
        # answering a solicited reattack
        reattack_comments_filled = [
            await _fill_vuln_info(
                loaders,
                comment,
                verification.vulnerability_ids,
                vulns,
            )
            if (
                comment.id == verification.comment_id
                and verification.vulnerability_ids
            )
            else None
            for comment in reattack_comments
            for verification in verified
        ]
        # Filter empty comments and remove duplicate reattack comments that can
        # happen if there is one replying to multiple reattacks
        unique_reattack_comments = list(
            set(
                comment
                for comment in reattack_comments_filled
                if comment is not None
            )
        )
        comments = unique_reattack_comments + non_reattack_comments

    enforcer = await authz.get_group_level_enforcer(loaders, user_email)
    if enforcer(group_name, "handle_comment_scope"):
        return tuple(comments)
    return tuple(filter(_is_scope_comment, comments))


async def get_observations(
    loaders: Dataloaders, group_name: str, finding_id: str, user_email: str
) -> list[FindingComment]:
    observations = await loaders.finding_comments.load(
        (CommentType.OBSERVATION, finding_id)
    )

    enforcer = await authz.get_group_level_enforcer(loaders, user_email)
    if enforcer(group_name, "handle_comment_scope"):
        return observations
    return list(filter(_is_scope_comment, observations))


def filter_reattack_comments(
    comments: list[FindingComment],
    verification_comment_ids: set[str],
) -> tuple[list[FindingComment], list[FindingComment]]:
    """Returns the comment list of a finding filtered on whether the comment
    answers a solicited reattack or not. Comments that do this will be within
    the first element of the tuple while the others will be in the second."""

    def filter_func(comment: FindingComment) -> bool:
        return comment.id in verification_comment_ids

    return list(filter(filter_func, comments)), list(
        filterfalse(filter_func, comments)
    )
