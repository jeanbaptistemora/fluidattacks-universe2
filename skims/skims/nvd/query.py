# Standard library
import re
from typing import (
    Callable,
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
from state.cache import (
    cache_decorator,
)
from utils.function import (
    shield,
)
from utils.model import (
    NVDVulnerability,
)

# Constants
TVar = TypeVar('TVar')
SHIELD: Callable[[TVar], TVar] = shield(
    retries=3,
    on_error_return=(),
    sleep_between_retries=5,
)
RE_CVE: Pattern = re.compile(r'vuln-detail-link-[0-9]+">(CVE-[0-9-]+)</a>')
RE_DESCRIPTION: Pattern = re.compile(r'vuln-summary-[0-9]+">([^<]*?)</p>')
RE_CVSS: Pattern = re.compile(
    r'vuln-cvss3-link-[0-9]+">([0-9.]*?) [A-Z]+</a>|\(not available\)',
)


@cache_decorator(ttl=86400)
@SHIELD
async def get_vulnerabilities(
    product: str,
    version: str,
    keywords: Tuple[str, ...] = (),
    target_software: str = '',
) -> Tuple[NVDVulnerability, ...]:
    cpe = build_cpe(
        keywords=keywords,
        product=product,
        target_software=target_software,
        version=version,
    )

    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=60.0),
        trust_env=True,
    ) as session:
        async with session.get(cpe) as response:
            response.raise_for_status()
            text = await response.text()

    return tuple(
        NVDVulnerability(
            code=code,
            cvss=cvss or '0.0',
            description=description,
            product=product,
            url=f'https://nvd.nist.gov/vuln/detail/{code}',
            version=version,
        )
        for code, cvss, description in zip(
            RE_CVE.findall(text),
            RE_CVSS.findall(text),
            RE_DESCRIPTION.findall(text),
        )
    )
