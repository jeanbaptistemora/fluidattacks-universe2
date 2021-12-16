from aiodataloader import (
    DataLoader,
)
from context import (
    FI_ENVIRONMENT,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from itertools import (
    chain,
)
import logging
from newutils import (
    vulnerabilities as vulns_utils,
)
from settings.logger import (
    NOEXTRA,
)
from typing import (
    List,
    Tuple,
)

LOGGER = logging.getLogger(__name__)
LOGGER_TRANSACTIONAL = logging.getLogger("transactional")


class FindingVulnsNonDeletedTypedLoader(DataLoader):
    def __init__(self, new_loader: DataLoader, old_loader: DataLoader) -> None:
        super().__init__()
        self.new_loader = new_loader
        self.old_loader = old_loader

    def clear(self, key: str) -> DataLoader:
        self.new_loader.clear(key)
        self.old_loader.clear(key)
        return super().clear(key)

    async def load_many_chained(
        self, finding_ids: List[str]
    ) -> Tuple[Vulnerability, ...]:
        unchained_data = await self.load_many(finding_ids)
        return tuple(chain.from_iterable(unchained_data))

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> Tuple[Tuple[Vulnerability, ...], ...]:
        if FI_ENVIRONMENT == "development":
            LOGGER_TRANSACTIONAL.info(
                ":".join(["Migration: Loading finding vulns", *finding_ids]),
                **NOEXTRA,
            )
            return await self.new_loader.load_many(finding_ids)

        findings_vulns = await self.old_loader.load_many(finding_ids)
        return tuple(
            vulns_utils.filter_non_deleted(finding_vulns)
            for finding_vulns in findings_vulns
        )
