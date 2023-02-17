from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
import aiofiles
from context import (
    FI_INTEGRATES_CRITERIA_VULNERABILITIES,
)
from typing import (
    Any,
    Iterable,
)
import yaml


async def _get_vulnerabilities_file() -> dict[str, Any]:
    """Parses the vulns info yaml from the repo into a dictionary."""
    async with aiofiles.open(
        FI_INTEGRATES_CRITERIA_VULNERABILITIES, encoding="utf-8"
    ) as handler:
        return yaml.safe_load(await handler.read())


class VulnerabilitiesFileLoader(DataLoader[str, dict[str, Any]]):
    # pylint: disable=method-hidden
    async def batch_load_fn(self, ids: Iterable[str]) -> list[dict[str, Any]]:
        return list(
            await collect(tuple(_get_vulnerabilities_file() for _ in ids))
        )
