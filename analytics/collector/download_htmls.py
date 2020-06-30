# Standard library
import asyncio
import os
from typing import (
    Dict,
)

# Third party libraries
import aiohttp

# Local libraries
from analytics import (
    utils,
)

# Finding bugs?
DEBUGGING: bool = False

# Constants
INTEGRATES_API_TOKEN: str = os.environ['INTEGRATES_API_TOKEN']
PROXY = 'http://127.0.0.1:8080' if DEBUGGING else None
SIZES = [
    # (Width, Height)
    [420, 160],
    [420, 320],
    [840, 480],
    [840, 600],
]


@utils.retry_on_exceptions(
    default_value=bytes(),
    exceptions=(
        aiohttp.ClientError,
    ),
    retry_times=5,
)
async def generate_html(
    *,
    document_name: str,
    document_type: str,
    generator_name: str,
    generator_type: str,
    entity: str,
    height: int,
    subject: str,
    width: int,
) -> bytes:
    connector = aiohttp.TCPConnector(ssl=False)
    timeout = aiohttp.ClientTimeout(
        total=None,
        connect=None,
        sock_connect=None,
        sock_read=None,
    )

    async with aiohttp.ClientSession(
        connector=connector,
        timeout=timeout,
    ) as session:
        url: str = 'https://fluidattacks.com/integrates/graphics'
        headers: Dict[str, str] = {
            'authorization': f'Bearer {INTEGRATES_API_TOKEN}'
        }
        params: Dict[str, str] = {
            'documentName': document_name,
            'documentType': document_type,
            'entity': entity,
            'generatorName': generator_name,
            'generatorType': generator_type,
            'height': str(height),
            'subject': subject,
            'width': str(width),
        }

        async with session.get(
            url,
            headers=headers,
            params=params,
            proxy=PROXY,
        ) as resp:
            return await resp.read()


async def collect():
    for width, height in SIZES:
        for document_type, document_name, generator_type, generator_name in [
            ['stackedBarChart', 'riskOverTime', 'c3', 'generic'],
            ['pieChart', 'treatment', 'c3', 'generic'],
            ['pieChart', 'status', 'c3', 'generic'],
            ['disjointForceDirectedGraph', 'whereToFindings',
             'disjointForceDirectedGraph', 'whereToFindings'],
        ]:
            for group in utils.iterate_groups():
                folder = (
                    f'analytics/collector/'
                    f'/{generator_type}/{generator_name}'
                    f'/{document_type}/{document_name}'
                    f'/group:{group}'
                )
                os.makedirs(folder, exist_ok=True)

                with open(f'{folder}/{width}x{height}.html', 'wb') as file:
                    file.write(await generate_html(
                        document_name=document_name,
                        document_type=document_type,
                        entity='group',
                        generator_name=generator_name,
                        generator_type=generator_type,
                        height=height,
                        subject=group,
                        width=width,
                    ))


if __name__ == '__main__':
    asyncio.run(collect())
