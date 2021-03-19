# Local libraries
from toe.lines import dal as toe_lines_dal
from dynamodb.types import GitRootToeLines


async def update(root_toe_lines: GitRootToeLines) -> None:
    await toe_lines_dal.update(root_toe_lines)
