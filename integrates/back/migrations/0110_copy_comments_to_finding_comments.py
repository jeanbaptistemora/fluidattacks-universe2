# pylint: disable=invalid-name
"""
This migration copy the comments table to the finding comments table
"""

from aioextensions import (
    collect,
    run,
)
from custom_types import (
    Comment,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from pprint import (
    pprint,
)

TABLE_NAME: str = "FI_comments"
TABLE_NAME_NEW: str = "fi_finding_comments"


async def copy_comment(comment: Comment) -> bool:
    comment.update(
        {
            "finding_id": str(comment.pop("finding_id")),
            "comment_id": str(comment.pop("user_id")),
        }
    )
    success = await dynamodb_ops.put_item(TABLE_NAME_NEW, comment)
    print(f'finding_id = {comment["finding_id"]}')
    print(f'comment_id = {comment["comment_id"]}')
    print("comment =")
    pprint(comment)
    return success


async def main() -> None:
    scan_attrs = {}
    comments = await dynamodb_ops.scan(TABLE_NAME, scan_attrs)
    success = all(
        await collect([copy_comment(comment) for comment in comments])
    )
    print(f"Success: {success}")


if __name__ == "__main__":
    run(main())
