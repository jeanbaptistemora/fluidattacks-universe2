from machine.jobs import (
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
