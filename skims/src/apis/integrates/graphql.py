# Third party libraries
from aiogqlc import GraphQLClient


def blocking_get_client(
    *,
    api_token: str,
    endpoint_url: str = 'https://fluidattacks.com/integrates/api',
) -> GraphQLClient:
    return GraphQLClient(
        endpoint=endpoint_url,
        headers={
            'authorization': f'Bearer {api_token}'
        },
    )
