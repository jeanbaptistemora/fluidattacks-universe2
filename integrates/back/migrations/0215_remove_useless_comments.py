# pylint: disable=invalid-name
"""
Remove useless comments on findings

Execution Time:    2022-05-17 at 20:17:47 UTCUTC
Finalization Time: 2022-05-17 at 21:01:58 UTCUTC
"""
from aioextensions import (
    run,
)
from dataloaders import (
    get_new_context,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingCommentsRequest,
)
from finding_comments import (
    domain as comments_domain,
)
import logging
import logging.config
from organizations.domain import (
    get_all_active_group_names,
)
import re
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")
TABLE_NAME: str = "FI_findings"


async def main() -> None:  # noqa: MC0001
    loaders = get_new_context()
    groups = sorted(await get_all_active_group_names(loaders=loaders))
    useless_comments = (
        r"^Reattack request was executed in\s\s\s\s\s\s\s\s\s\s\s\s\s"
        + r"+([0-9]{4}\/+[0-9]{2}\/+[0-9]{2}\s"
        + r"[0-9]{2}\:[0-9]{2})\.\s$"
    )

    for group in groups:
        findings = await loaders.group_findings.load(group)

        for finding_id in [finding.id for finding in findings]:
            comments = await loaders.finding_comments.load(
                FindingCommentsRequest(
                    comment_type=CommentType.COMMENT, finding_id=finding_id
                )
            )
            for comment in comments:
                if comment.email == "machine@fluidattacks.com":
                    if re.search(useless_comments, comment.content):
                        await comments_domain.remove(  # type: ignore
                            comment.id, finding_id
                        )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
