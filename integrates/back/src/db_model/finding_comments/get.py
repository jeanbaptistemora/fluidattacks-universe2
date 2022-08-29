from .types import (
    FindingComment,
)
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
from db_model import (
    TABLE,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.utils import (
    format_finding_comments,
)
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Iterable,
)


async def _get_comments(
    *, comment_type: CommentType, finding_id: str
) -> tuple[FindingComment, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_comment"],
        values={"finding_id": finding_id},
    )

    key_structure = TABLE.primary_key
    if comment_type == CommentType.COMMENT:
        filter_expression = Attr("comment_type").eq("COMMENT") | Attr(
            "comment_type"
        ).eq("VERIFICATION")
    else:
        filter_expression = Attr("comment_type").eq(comment_type.value)
    response = await operations.query(
        filter_expression=filter_expression,
        condition_expression=(
            Key(key_structure.sort_key).eq(primary_key.sort_key)
            & Key(key_structure.partition_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["finding_comment"],),
        index=TABLE.indexes["inverted_index"],
        table=TABLE,
    )
    return tuple(format_finding_comments(item) for item in response.items)


class FindingCommentsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, comments: Iterable[tuple[CommentType, str]]
    ) -> tuple[tuple[FindingComment, ...], ...]:
        return await collect(
            tuple(
                _get_comments(comment_type=comment_type, finding_id=finding_id)
                for comment_type, finding_id in comments
            )
        )
