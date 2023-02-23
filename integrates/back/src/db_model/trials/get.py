from .types import (
    Trial,
)
from .utils import (
    format_trial,
)
from aiodataloader import (
    DataLoader,
)
from collections.abc import (
    Iterable,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)


async def _get_trials(emails: Iterable[str]) -> list[Trial]:
    primary_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["trial_metadata"],
            values={"all": "all", "email": email},
        )
        for email in emails
    )
    items = await operations.batch_get_item(keys=primary_keys, table=TABLE)

    return [format_trial(item) for item in items]


class TrialLoader(DataLoader[str, Trial | None]):
    # pylint: disable=method-hidden
    async def batch_load_fn(self, emails: Iterable[str]) -> list[Trial | None]:
        trials = {trial.email: trial for trial in await _get_trials(emails)}

        return [trials.get(email) for email in emails]
