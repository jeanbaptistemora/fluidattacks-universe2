"""Fluidattacks Forces package."""
# Standard imports
import asyncio
from contextvars import ContextVar

# 3d Impors
from gql import AIOHTTPTransport, Client

# Local imports
from forces.apis.integrates import get_findings
from forces.apis.integrates import get_vulnerabilities

# Constants
INTEGRATES_API_URL: str = 'https://fluidattacks.com/integrates/api'
INTEGRATES_API_TOKEN: ContextVar[str] = ContextVar('integrates_api_token')


def set_api_token(token: str) -> None:
    """Set value for integrates API token."""
    INTEGRATES_API_TOKEN.set(token)


async def _async_process(project: str) -> None:
    transport = AIOHTTPTransport(
        url=INTEGRATES_API_URL,
        headers={'Authorization': f'Bearer {INTEGRATES_API_TOKEN.get()}'},
        timeout=60)
    async with Client(
            transport=transport,
            fetch_schema_from_transport=True,
    ) as client:
        findings = await get_findings(client, project)
        finds_vulns = [get_vulnerabilities(client, fin) for fin in findings]
        for find_vuln in asyncio.as_completed(finds_vulns):
            status = []
            find, vulns = await find_vuln
            for vuln in vulns:
                historic_state = vuln['historicState']
                is_open = historic_state[-1]['state'] not in (  # type: ignore
                    'closed', 'accepted')
                status.append(is_open)
            if any(status):
                print(f'# Find {find} is open')


def process(project: str) -> None:
    asyncio.run(_async_process(project))
