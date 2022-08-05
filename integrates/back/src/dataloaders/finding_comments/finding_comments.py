from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from db_model.finding_comments.types import (
    FindingComment,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from newutils.finding_comments import (
    format_finding_comments,
)
from typing import (
    Any,
    Iterable,
)

TABLE_NAME: str = "fi_finding_comments"


async def get_comments(
    comment_type: str, finding_id: str
) -> list[dict[str, Any]]:
    """Get comments of the given finding"""
    key_exp = Key("finding_id").eq(finding_id)
    comment_type = comment_type.lower()
    filter_exp = ""
    if comment_type == "comment":
        filter_exp = Attr("comment_type").eq("comment") | Attr(
            "comment_type"
        ).eq("verification")
    elif comment_type == "observation":
        filter_exp = Attr("comment_type").eq("observation")
    elif comment_type == "zero_risk":
        filter_exp = Attr("comment_type").eq("zero_risk")
    query_attrs = {
        "KeyConditionExpression": key_exp,
        "FilterExpression": filter_exp,
    }
    return await dynamodb_ops.query(TABLE_NAME, query_attrs)


class FindingCommentsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, keys: Iterable[tuple[str, str]]
    ) -> tuple[tuple[FindingComment, ...], ...]:
        items = await collect(
            tuple(
                (
                    get_comments(
                        comment_type=comment_type, finding_id=finding_id
                    )
                    for comment_type, finding_id in keys
                )
            )
        )
        return tuple(
            tuple(format_finding_comments(item=item) for item in lst)
            for lst in items
        )
