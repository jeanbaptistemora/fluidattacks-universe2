# Third party libraries
from aiogqlc import GraphQLClient


class Session():
    # pylint: disable=too-few-public-methods
    value: GraphQLClient = None


def create_session(
    *,
    api_token: str,
    endpoint_url: str = 'https://fluidattacks.com/integrates/api',
) -> None:
    Session.value = GraphQLClient(
        endpoint=endpoint_url,
        headers={
            'authorization': f'Bearer {api_token}'
        },
    )
