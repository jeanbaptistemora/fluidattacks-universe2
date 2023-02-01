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
from db_model.finding_comments.types import (
    FindingCommentsRequest,
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
) -> list[FindingComment]:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_comment"],
        values={"finding_id": finding_id},
    )
    key_structure = TABLE.primary_key
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

    return [format_finding_comments(item) for item in response.items]


class FindingCommentsLoader(
    DataLoader[FindingCommentsRequest, list[FindingComment]]
):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[FindingCommentsRequest]
    ) -> list[list[FindingComment]]:
        return list(
            await collect(
                _get_comments(
                    comment_type=request.comment_type,
                    finding_id=request.finding_id,
                )
                for request in requests
            )
        )
