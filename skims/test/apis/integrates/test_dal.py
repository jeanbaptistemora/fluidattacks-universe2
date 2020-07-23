# Third party libraries
import pytest

# Local libraries
from apis.integrates.dal import (
    get_finding_vulnerabilities,
    get_group_findings,
    get_group_level_role,
    do_upload_vulnerabilities,
    ResultGetGroupFindings,
)
from apis.integrates.graphql import (
    session,
)
from model import (
    FindingEnum,
    KindEnum,
    Vulnerability,
    VulnerabilityStateEnum,
)


@pytest.mark.asyncio  # type: ignore
async def test_dal(
    test_group: str,
    test_token: str,
) -> None:
    async with session(api_token=test_token):
        assert await get_group_level_role(group=test_group) == 'admin'

        assert ResultGetGroupFindings(
            identifier='974751758',
            title='FIN.S.0034. Insecure random numbers generation',
        ) in await get_group_findings(group=test_group)

        assert await do_upload_vulnerabilities(
            finding_id='974751758',
            stream="""
                inputs: []
                lines: []
                ports:
                    -   host: 127.0.0.1
                        port: '80'
                        state: open
            """,
        )

        assert Vulnerability(
            finding=FindingEnum.F0034,
            kind=KindEnum.PORTS,
            state=VulnerabilityStateEnum.OPEN,
            what='127.0.0.1',
            where='80',
        ) in await get_finding_vulnerabilities(
            finding=FindingEnum.F0034,
            finding_id='974751758',
        )
