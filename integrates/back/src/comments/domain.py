from aioextensions import (
    collect,
)
import authz
from comments import (
    dal as comments_dal,
)
from custom_types import (
    Comment as CommentType,
    Finding as FindingType,
    User as UserType,
)
from datetime import (
    datetime,
)
from db_model.findings.types import (
    FindingVerification,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from itertools import (
    filterfalse,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    cast,
    Dict,
    List,
    Set,
    Tuple,
    Union,
)


def _fill_vuln_info(
    comment: Dict[str, str],
    vulns_ids: Set[str],
    vulns: List[Dict[str, FindingType]],
) -> CommentType:
    """Adds the «Regarding vulnerabilities...» header to comments answering a
    solicited reattack"""
    selected_vulns = [
        vuln.get("where") for vuln in vulns if vuln.get("UUID") in vulns_ids
    ]
    selected_vulns = list(set(selected_vulns))
    wheres = ", ".join(cast(List[str], selected_vulns))
    # Avoid needless repetition of the header if the comment is answering more
    # than one reattack
    if not comment.get("content", "").startswith(
        f"Regarding vulnerabilities {wheres}:"
    ):
        comment[
            "content"
        ] = f"Regarding vulnerabilities {wheres}:\n\n" + comment.get(
            "content", ""
        )
    return cast(CommentType, comment)


async def _fill_comment_data(data: Dict[str, str]) -> CommentType:
    fullname = await _get_fullname(objective_data=data)
    return {
        "content": data["content"],
        "created": datetime_utils.format_comment_date(data["created"]),
        "email": data["email"],
        "fullname": fullname if fullname else data["email"],
        "id": data["comment_id"],
        "modified": datetime_utils.format_comment_date(data["modified"]),
        "parent": data["parent"],
    }


async def _get_comments(
    comment_type: str,
    finding_id: str,
) -> List[CommentType]:
    comments = await collect(
        [
            _fill_comment_data(cast(Dict[str, str], comment))
            for comment in await comments_dal.get_comments(
                comment_type, finding_id
            )
        ]
    )
    return list(comments)


async def _get_fullname(objective_data: Dict[str, str]) -> str:
    objective_email = objective_data["email"]
    objective_possible_fullname = objective_data.get("fullname", "")
    real_name = objective_possible_fullname or objective_email

    if "@fluidattacks.com" in objective_email:
        return f"{real_name} at Fluid Attacks"

    return real_name


def _is_scope_comment(comment: CommentType) -> bool:
    return str(comment["content"]).strip() not in {"#external", "#internal"}


async def add(
    finding_id: str, comment_data: CommentType, user_info: UserType
) -> Tuple[Union[str, None], bool]:
    today = datetime_utils.get_as_str(datetime_utils.get_now())
    comment_id = str(comment_data["comment_id"])
    comment_attributes = {
        "comment_type": comment_data["comment_type"],
        "content": str(comment_data.get("content")),
        "created": today,
        "email": user_info["user_email"],
        "fullname": str.join(
            " ", [str(user_info["first_name"]), str(user_info["last_name"])]
        ),
        "modified": today,
        "parent": comment_data.get("parent", "0"),
    }
    success = await comments_dal.create(
        comment_id, comment_attributes, finding_id
    )
    return (comment_id if success else None, success)


async def delete(comment_id: str, finding_id: str) -> bool:
    return await comments_dal.delete(comment_id, finding_id)


async def get(comment_type: str, element_id: str) -> List[CommentType]:
    return await comments_dal.get_comments(comment_type, element_id)


async def get_comments(
    group_name: str,
    finding_id: str,
    user_email: str,
    info: GraphQLResolveInfo,
) -> List[CommentType]:
    finding_loader = info.context.loaders.finding
    finding_vulns_loader = info.context.loaders.finding_vulns

    comments = await _get_comments("comment", finding_id)
    finding = await finding_loader.load(finding_id)
    historic_verification = finding.get("historic_verification", [])
    verified = [
        verification
        for verification in historic_verification
        if cast(List[str], verification.get("vulns", []))
    ]
    if verified:
        vulns = await finding_vulns_loader.load(finding_id)
        verification_comment_ids: Set[str] = {
            str(verification["comment"]) for verification in verified
        }
        reattack_comments, non_reattack_comments = filter_reattack_comments(
            comments, verification_comment_ids
        )

        # Loop to add the «Regarding vulnerabilities...» header to comments
        # answering a solicited reattack
        reattack_comments = [
            _fill_vuln_info(
                cast(Dict[str, str], comment),
                set(cast(List[str], verification.get("vulns", []))),
                vulns,
            )
            if str(comment["id"]) == str(verification["comment"])
            else {}
            for comment in reattack_comments
            for verification in verified
        ]
        reattack_comments = list(filter(None, reattack_comments))
        comments = reattack_comments + non_reattack_comments

    enforcer = await authz.get_group_level_enforcer(user_email)
    if enforcer(group_name, "handle_comment_scope"):
        return comments
    return list(filter(_is_scope_comment, comments))


async def get_comments_new(
    group_name: str, finding_id: str, user_email: str, info: GraphQLResolveInfo
) -> Tuple[CommentType, ...]:
    historic_verification_loader = (
        info.context.loaders.finding_historic_verification_new
    )
    finding_vulns_loader = info.context.loaders.finding_vulns
    comments = await _get_comments("comment", finding_id)
    historic_verification: Tuple[
        FindingVerification, ...
    ] = await historic_verification_loader.load(finding_id)
    verified = tuple(
        verification
        for verification in historic_verification
        if verification.vulnerability_ids
    )
    if bool(verified):
        verification_comment_ids: Set[str] = {
            verification.comment_id for verification in verified
        }
        vulns = await finding_vulns_loader.load(finding_id)
        reattack_comments, non_reattack_comments = filter_reattack_comments(
            comments, verification_comment_ids
        )
        # Loop to add the «Regarding vulnerabilities...» header to comments
        # answering a solicited reattack
        reattack_comments = [
            _fill_vuln_info(
                cast(Dict[str, str], comment),
                verification.vulnerability_ids,
                vulns,
            )
            if comment["id"] == verification.comment_id
            else {}
            for comment in reattack_comments
            for verification in verified
        ]
        # Filter empty comments and remove duplicate reattack comments that can
        # happen if there is one replying to multiple reattacks
        reattack_comments = list(filter(None, reattack_comments))
        unique_reattack_comments = list(
            {comment["id"]: comment for comment in reattack_comments}.values()
        )
        comments = unique_reattack_comments + non_reattack_comments

    enforcer = await authz.get_group_level_enforcer(user_email)
    if enforcer(group_name, "handle_comment_scope"):
        return tuple(comments)
    return tuple(filter(_is_scope_comment, comments))


async def get_event_comments(
    group_name: str, finding_id: str, user_email: str
) -> List[CommentType]:
    comments = await _get_comments("event", finding_id)

    new_comments: List[CommentType] = []
    enforcer = await authz.get_group_level_enforcer(user_email)
    if enforcer(group_name, "handle_comment_scope"):
        new_comments = comments
    else:
        new_comments = list(filter(_is_scope_comment, comments))
    return new_comments


async def get_observations(
    group_name: str, finding_id: str, user_email: str
) -> List[CommentType]:
    observations = await _get_comments("observation", finding_id)

    new_observations: List[CommentType] = []
    enforcer = await authz.get_group_level_enforcer(user_email)
    if enforcer(group_name, "handle_comment_scope"):
        new_observations = observations
    else:
        new_observations = list(filter(_is_scope_comment, observations))
    return new_observations


def filter_comments_date(
    comments: List[CommentType],
    min_date: datetime,
) -> List[CommentType]:
    return [
        comment
        for comment in comments
        if min_date
        and datetime_utils.get_from_str(comment["created"]) >= min_date
    ]


def filter_reattack_comments(
    comments: List[CommentType],
    verification_comment_ids: Set[str],
) -> Tuple[List[CommentType], List[CommentType]]:
    """Returns the comment list of a finding filtered on whether the comment
    answers a solicited reattack or not. Comments that do this will be within
    the first element of the tuple while the others will be in the second"""

    def filter_func(comment: CommentType) -> bool:
        return str(comment["id"]) in verification_comment_ids

    return list(filter(filter_func, comments)), list(
        filterfalse(filter_func, comments)
    )
