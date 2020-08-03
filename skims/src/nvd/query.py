# Standard library
import re
import socket
from typing import (
    Callable,
    NamedTuple,
    Pattern,
    Tuple,
    TypeVar,
)

# Third party libraries
import aiohttp

# Local libraries
from nvd.cpe import (
    build as build_cpe,
)
from utils.function import (
    retry,
)
from utils.logs import (
    log,
)

# Constants
TVar = TypeVar('TVar')
RETRY: Callable[[TVar], TVar] = retry(
    attempts=12,
    on_exceptions=(
        aiohttp.ClientError,
        IndexError,
        socket.gaierror,
    ),
)
RE_CVE: Pattern = re.compile(r'vuln-detail-link-[0-9]+">(CVE-[0-9-]+)</a>')
RE_DESCRIPTION: Pattern = re.compile(r'vuln-summary-[0-9]+">([^<]*?)</p>')


class CVE(NamedTuple):
    code: str
    description: str
    url: str


@RETRY
async def get_vulnerabilities(
    product: str,
    version: str,
    keywords: Tuple[str, ...] = (),
    target_software: str = '',
) -> Tuple[CVE, ...]:
    cpe = build_cpe(
        keywords=keywords,
        product=product,
        target_software=target_software,
        version=version,
    )

    await log('info', 'cpe: %s', cpe)

    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=60.0),
        trust_env=True,
    ) as session:
        async with session.get(cpe) as response:
            response.raise_for_status()
            text = await response.text()

    return tuple(
        CVE(
            code=code,
            description=description,
            url=f'https://nvd.nist.gov/vuln/detail/{code}'
        )
        for code, description in zip(
            RE_CVE.findall(text),
            RE_DESCRIPTION.findall(text),
        )
    )
