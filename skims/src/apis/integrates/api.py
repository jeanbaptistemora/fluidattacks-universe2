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
