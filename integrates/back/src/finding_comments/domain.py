import authz
from db_model.finding_comments.types import (
    FindingComment,
)
from db_model.findings.types import (
    FindingVerification,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from finding_comments import (
    dal as comments_dal,
)
from itertools import (
    filterfalse,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Any,
    Dict,
    List,
    Set,
    Tuple,
    Union,
)


def _fill_vuln_info(
    comment: FindingComment,
    vulns_ids: Set[str],
    vulns: Tuple[Vulnerability, ...],
) -> FindingComment:
    """Adds the «Regarding vulnerabilities...» header to comments answering a
    solicited reattack"""
    selected_vulns = [
        f"  - {vuln.where}" for vuln in vulns if vuln.id in vulns_ids
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


def _is_scope_comment_typed(comment: FindingComment) -> bool:
    return comment.content.strip() not in {"#external", "#internal"}


async def add(
    finding_id: str,
    comment_data: Dict[str, Any],
    user_info: Stakeholder,
) -> Tuple[Union[str, None], bool]:
    today = datetime_utils.get_as_str(datetime_utils.get_now())
    comment_id = str(comment_data["comment_id"])
    comment_attributes = {
        "comment_type": comment_data["comment_type"],
        "content": str(comment_data.get("content")),
        "created": today,
        "email": user_info.email,
        "fullname": str.join(" ", [user_info.first_name, user_info.last_name])
        if user_info.first_name and user_info.last_name
        else "",
        "modified": today,
        "parent": comment_data.get("parent", "0"),
    }
    success = await comments_dal.create(
        comment_id, comment_attributes, finding_id
    )
    return (comment_id if success else None, success)


async def delete(comment_id: str, finding_id: str) -> bool:
    return await comments_dal.delete(comment_id, finding_id)


async def get(comment_type: str, element_id: str) -> List[Dict[str, Any]]:
    return await comments_dal.get_comments(comment_type, element_id)


async def get_comments(
    loaders: Any,
    group_name: str,
    finding_id: str,
    user_email: str,
) -> Tuple[FindingComment, ...]:
    comments = await loaders.finding_comments.load(("comment", finding_id))
    historic_verification: Tuple[
        FindingVerification, ...
    ] = await loaders.finding_historic_verification.load(finding_id)
    verified = tuple(
        verification
        for verification in historic_verification
        if verification.vulnerability_ids
    )
    if bool(verified):
        verification_comment_ids: Set[str] = {
            verification.comment_id for verification in verified
        }
        vulns: Tuple[
            Vulnerability, ...
        ] = await loaders.finding_vulnerabilities.load(finding_id)

        reattack_comments, non_reattack_comments = filter_reattack_comments(
            comments, verification_comment_ids
        )
        # Loop to add the «Regarding vulnerabilities...» header to comments
        # answering a solicited reattack
        reattack_comments_filled = [
            _fill_vuln_info(
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

    enforcer = await authz.get_group_level_enforcer(user_email)
    if enforcer(group_name, "handle_comment_scope"):
        return tuple(comments)
    return tuple(filter(_is_scope_comment_typed, comments))


async def get_observations(
    loaders: Any, group_name: str, finding_id: str, user_email: str
) -> list[FindingComment]:
    observations = await loaders.finding_comments.load(
        ("observation", finding_id)
    )

    enforcer = await authz.get_group_level_enforcer(user_email)
    if enforcer(group_name, "handle_comment_scope"):
        return observations
    return list(filter(_is_scope_comment_typed, observations))


def filter_reattack_comments(
    comments: List[FindingComment],
    verification_comment_ids: Set[str],
) -> Tuple[List[FindingComment], List[FindingComment]]:
    """Returns the comment list of a finding filtered on whether the comment
    answers a solicited reattack or not. Comments that do this will be within
    the first element of the tuple while the others will be in the second"""

    def filter_func(comment: FindingComment) -> bool:
        return comment.id in verification_comment_ids

    return list(filter(filter_func, comments)), list(
        filterfalse(filter_func, comments)
    )
