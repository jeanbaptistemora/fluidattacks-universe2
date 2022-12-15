from datetime import (
    datetime,
)
from db_model.roots.types import (
    MachineFindingResult,
    RootMachineExecution,
)
from machine.jobs import (
    _get_job_execution_time,
    _get_priority_suffix,
    get_finding_code_from_title,
    get_queue_for_finding,
)


def test_get_priotiry_suffix() -> None:
    urgent_no: bool = False
    priotiry_suffix_no_urg = _get_priority_suffix(urgent_no)
    assert priotiry_suffix_no_urg == "later"
    urgent_yes: bool = True
    priotiry_suffix_urg = _get_priority_suffix(urgent_yes)
    assert priotiry_suffix_urg == "soon"


def test_get_queue_for_finding() -> None:
    finding_code: str = "F046"
    urgent: bool = True
    queue = get_queue_for_finding(finding_code, urgent)
    assert queue == "skims_apk_soon"


def test_get_finding_code_from_title() -> None:
    spec_finding_code: str = "F416"
    finding_title: str = "416. XAML injection"
    finding_code = get_finding_code_from_title(finding_title)
    assert finding_code == spec_finding_code


def test_get_job_execution_time() -> None:
    job_id = "test"
    name = "skims-jobtest-unittesting"
    created_at = datetime.fromisoformat("2020-01-01T01:00:00+00:00")
    started_at = datetime.fromisoformat("2020-01-01T01:10:00+00:00")
    finding1 = MachineFindingResult(
        open=0,
        modified=0,
        finding="F001",
    )
    finding2 = MachineFindingResult(
        open=0,
        modified=0,
        finding="F002",
    )
    findings = [finding1, finding2]
    job_execution_for_test = RootMachineExecution(
        job_id="",
        name=name,
        findings_executed=findings,
        queue="small",
        root_id="",
        created_at=created_at,
        started_at=started_at,
    )
    jobs_dict = {job_id: job_execution_for_test}
    time = _get_job_execution_time(
        job_execution_for_test.started_at,
        "startedAt",
        jobs_dict,
        job_execution_for_test,
    )
    assert time == 1577841000000
