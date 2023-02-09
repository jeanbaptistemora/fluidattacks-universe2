from dataloaders import (
    get_new_context,
)
from db_model.trials.types import (
    TrialMetadataToUpdate,
)
import pytest
from schedulers.reminder_notification import (
    is_trial_end,
)
from trials import (
    domain as trials_domain,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "emails",
        "outputs",
    ],
    [
        [
            ["notregistered@unknown.com", "unittest@fluidattacks.com"],
            [False, True],
        ],
    ],
)
async def test_is_trial_end(emails: list[str], outputs: list[bool]) -> None:
    loaders = get_new_context()
    for index, email in enumerate(emails):
        assert await is_trial_end(loaders, email) == outputs[index]

    await trials_domain.update_metadata(
        email=emails[1],
        metadata=TrialMetadataToUpdate(completed=False),
    )
    assert await is_trial_end(get_new_context(), emails[1]) == outputs[0]
