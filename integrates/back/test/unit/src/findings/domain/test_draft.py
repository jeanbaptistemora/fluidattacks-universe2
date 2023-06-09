# pylint: disable=import-error
from back.test.unit.src.utils import (
    create_dummy_info,
    create_dummy_session,
)
from custom_exceptions import (
    AlreadyApproved,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from findings.domain import (
    approve_draft,
)
from freezegun import (
    freeze_time,
)
from newutils import (
    requests as requests_utils,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
@freeze_time("2019-12-01")
async def test_approve_draft() -> None:  # pylint: disable=too-many-locals
    finding_id = "475041513"
    approved_finding_id = "457497318"
    user_email = "unittest@fluidattacks.com"
    request = await create_dummy_session(user_email)
    info = create_dummy_info(request)
    loaders: Dataloaders = info.context.loaders
    historic_state_loader = loaders.vulnerability_historic_state
    historic_treatment_loader = loaders.vulnerability_historic_treatment
    with pytest.raises(AlreadyApproved):
        await approve_draft(
            loaders,
            approved_finding_id,
            user_email,
            requests_utils.get_source_new(info.context),
        )

    approval_date = await approve_draft(
        loaders,
        finding_id,
        user_email,
        requests_utils.get_source_new(info.context),
    )
    expected_date = datetime.fromisoformat("2019-12-01T00:00:00+00:00")
    assert isinstance(approval_date, datetime)
    assert approval_date == expected_date

    all_vulns = await loaders.finding_vulnerabilities_all.load(finding_id)
    vuln_ids = [vuln.id for vuln in all_vulns]

    for vuln_id in vuln_ids:
        historic_state_loader.clear(vuln_id)
        historic_state = await historic_state_loader.load(vuln_id)
        for state in historic_state:
            assert state.modified_date == expected_date

        historic_treatment_loader.clear(vuln_id)
        historic_treatment = await historic_treatment_loader.load(vuln_id)
        for treatment in historic_treatment:
            assert treatment.modified_date == expected_date
