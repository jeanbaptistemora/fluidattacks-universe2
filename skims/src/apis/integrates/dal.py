# Standard library
from typing import (
    Any,
    Dict,
    NamedTuple,
    Tuple,
)

# Local libraries
from apis.integrates.graphql import (
    SESSION,
)
from utils.function import (
    retry,
)


async def _execute(*, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
    response = await SESSION.get().execute(query=query, variables=variables)

    result: Dict[str, Any] = await response.json()

    return result


@retry()
async def get_group_level_role(
    *,
    group: str,
) -> str:
    result = await _execute(
        query="""
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
        """,
        variables=dict(
            group=group,
        )
    )

    role: str = result['data']['me']['role']

    return role


class ResultGetGroupFindings(NamedTuple):
    identifier: str
    title: str


@retry()
async def get_group_findings(
    *,
    group: str,
) -> Tuple[ResultGetGroupFindings, ...]:
    result = await _execute(
        query="""
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
        """,
        variables=dict(
            group=group,
        )
    )

    return tuple(
        ResultGetGroupFindings(
            identifier=finding['id'],
            title=finding['title'],
        )
        for finding in result['data']['project']['findings']
    )
