# pylint: disable=invalid-name
"""
This migration set the finding comment parent as string since
the parent is a comment_id
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
from typing import (
    Any,
    Dict,
)

TABLE_NAME_NEW: str = "fi_finding_comments"


async def set_parent_as_string(comment: Comment) -> bool:
    comment.update(
        {
            "parent": str(comment["parent"]),
        }
    )
    success = await dynamodb_ops.put_item(TABLE_NAME_NEW, comment)
    print(f'finding_id = {comment["finding_id"]}')
    print(f'comment_id = {comment["comment_id"]}')
    print("comment =")
    pprint(comment)
    return success


async def main() -> None:
    scan_attrs: Dict[str, Any] = {}
    comments = await dynamodb_ops.scan(TABLE_NAME_NEW, scan_attrs)
    success = all(
        await collect([set_parent_as_string(comment) for comment in comments])
    )
    print(f"Success: {success}")


if __name__ == "__main__":
    run(main())
