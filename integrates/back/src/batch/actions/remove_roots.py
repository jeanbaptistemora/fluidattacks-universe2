from aioextensions import (
    collect,
)
import asyncio
from batch.types import (
    BatchProcessing,
)
from typing import (
    List,
)


async def remove_roots(*, item: BatchProcessing) -> None:
    group_name: str = item.entity
    root_nicknames: List[str] = item.additional_info.split(",")
    await collect(
        [
            asyncio.create_subprocess_exec(
                "aws",
                "s3",
                "rm",
                f"s3://continuous-repositories/{group_name}/{nickname}*",
            )
            for nickname in root_nicknames
        ]
    )
