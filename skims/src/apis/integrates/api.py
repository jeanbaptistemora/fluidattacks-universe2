# Standard library
from typing import (
    NamedTuple,
    Tuple,
)

# Third party libraries
from gql import (
    gql,
)

# Local libraries
from apis.integrates.graphql import (
    SESSION,
)
from utils.function import (
    retry,
)


@retry()
async def get_group_level_role(
    *,
    group: str,
) -> str:
    result = await SESSION.get().execute(
        document=gql("""
            query GetGroupLevelRole(
                $group: String!
            ) {
                me {
                    role(
                        entity: PROJECT
                        identifier: $group
                    )
                }
            }
        """),
        variable_values=dict(
            group=group,
        )
    )

    return result['me']['role']


class ResultGetGroupFindings(NamedTuple):
    identifier: str
    title: str


@retry()
async def get_group_findings(
    *,
    group: str,
) -> Tuple[ResultGetGroupFindings, ...]:
    result = await SESSION.get().execute(
        document=gql("""
            query GetGroupFindings(
                $group: String!
            ) {
                project(projectName: $group) {
                    findings {
                        id
                        title
                    }
                }
            }
        """),
        variable_values=dict(
            group=group,
        )
    )

    return tuple(
        ResultGetGroupFindings(
            identifier=finding['id'],
            title=finding['title'],
        )
        for finding in result['project']['findings']
    )
