# Third party libraries
import pytest

# Local libraries
from apis.integrates.domain import (
    get_closest_finding_id,
)
from apis.integrates.graphql import (
    session,
)


@pytest.mark.asyncio  # type: ignore
async def test_domain(
    test_group: str,
    test_token: str,
) -> None:
    async with session(api_token=test_token):
        assert await get_closest_finding_id(
            group=test_group,
            title='Insecure random numbers generation',
        ) == '974751758'

        assert await get_closest_finding_id(
            group=test_group,
            title='XXX',
        ) == ''
