# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from batch.enums import (
    Action,
)
from batch.types import (
    BatchProcessing,
)
from batch_dispatch import (
    rebase,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from newutils.datetime import (
    get_as_epoch,
    get_now,
)
import pytest
from typing import (
    Any,
    Dict,
)
from vulnerabilities.domain.snippet import (
    snippet_already_exists,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch_dispatch_s3")
async def test_clone_roots_real_ssh(
    generic_data: Dict[str, Any],
) -> None:
    loaders: Dataloaders = get_new_context()

    assert (
        await loaders.vulnerability.load(
            "4dbc03e0-4cfc-4b33-9b70-bb7566c460bd"
        )
    ).specific == "5"
    action = BatchProcessing(
        action_name=Action.REBASE.value,
        entity="unittesting",
        subject=generic_data["global_vars"]["admin_email"],
        time=str(get_as_epoch(get_now())),
        additional_info="nickname1",
        batch_job_id=None,
        queue="small",
        key="2",
    )
    await rebase.rebase(item=action)
    loaders.vulnerability.clear_all()
    vuln: Vulnerability = await loaders.vulnerability.load(
        "4dbc03e0-4cfc-4b33-9b70-bb7566c460bd"
    )
    assert vuln.specific == "11"  # this line has been changed
    assert (
        await loaders.vulnerability.load("4dbc01e0-4cfc-4b77-9b71-bb7566c60bg")
    ).specific == "3"
    assert await snippet_already_exists(vuln.id, vuln.state.modified_date)
