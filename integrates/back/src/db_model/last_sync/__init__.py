# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    _queries,
)
from ._queries import (
    RepoId,
)
from context import (
    FI_ENVIRONMENT,
)
from dataclasses import (
    dataclass,
)
import logging
import logging.config
from psycopg2.extensions import (
    cursor as cursor_cls,
)
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class LastUpdateClient:
    cursor: cursor_cls

    def exist(self, repo: RepoId) -> bool:
        if FI_ENVIRONMENT == "production":
            query = _queries.get(repo)
            self.cursor.execute(query.query_info, query.values)
            result = self.cursor.fetchall()
            return bool(result)
        LOGGER.debug("DRY-RUN: exist last update indicator for %s", repo)
        return False

    def upsert_indicator(self, repo: RepoId) -> None:
        if FI_ENVIRONMENT == "production":
            query = (
                _queries.update(repo)
                if self.exist(repo)
                else _queries.insert(repo)
            )
            self.cursor.execute(query.query_info, query.values)
        else:
            LOGGER.debug("DRY-RUN: refresh last update indicator for %s", repo)


__all__ = [
    "RepoId",
]
