from dataloaders import (
    get_new_context,
)
from organizations.domain import (
    get_all_active_group_names,
)
import pytest
from schedulers.machine_queue_all import (
    main as schedule_main,
)
from unittest.mock import (
    patch,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("machine_queue_all")
async def test_scheduler(
    populate: bool, caplog: pytest.LogCaptureFixture
) -> None:
    assert populate

    loaders = get_new_context()
    groups = await get_all_active_group_names(loaders)
    assert len(groups) == 2

    with patch(
        "schedulers.machine_queue_all.queue_job_new", return_value=None
    ):
        await schedule_main()
        assert len(caplog.records) == 1
        assert caplog.records[0].levelname == "INFO"
        assert (
            "Queueing 1 roots for group machinegroup: [activeroot]"
            in caplog.text
        )
