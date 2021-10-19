from model import (
    core_model,
)
import pytest
from typing import (
    List,
)
from zone import (
    t,
)


@pytest.mark.skims_test_group("unittesting")
def test_model_core_model_from_integrates() -> None:
    assert ("", "test") == core_model.Vulnerability.what_from_integrates(
        kind=core_model.VulnerabilityKindEnum.INPUTS,
        what_on_integrates="test",
    )
    assert ("", "test") == core_model.Vulnerability.what_from_integrates(
        kind=core_model.VulnerabilityKindEnum.LINES,
        what_on_integrates="test",
    )
    assert ("", "test") == core_model.Vulnerability.what_from_integrates(
        kind=core_model.VulnerabilityKindEnum.PORTS,
        what_on_integrates="test",
    )
    assert ("ns", "test()") == core_model.Vulnerability.what_from_integrates(
        kind=core_model.VulnerabilityKindEnum.INPUTS,
        what_on_integrates="test() (ns)",
    )
    assert ("ns", "te/st") == core_model.Vulnerability.what_from_integrates(
        kind=core_model.VulnerabilityKindEnum.LINES,
        what_on_integrates="ns/te/st",
    )
    assert ("ns", "test()") == core_model.Vulnerability.what_from_integrates(
        kind=core_model.VulnerabilityKindEnum.PORTS,
        what_on_integrates="test() (ns)",
    )


def _get_findings_title(locale: core_model.LocalesEnum) -> List[str]:
    return [
        t(finding.value.title, locale=locale)
        for finding in core_model.FindingEnum
    ]
