from itertools import (
    combinations,
)
import json
from model import (
    core_model,
)
import pytest
from typing import (
    List,
)
from utils.ctx import (
    SHOULD_UPDATE_TESTS,
)
from utils.string import (
    similar_ratio,
)
from zone import (
    t,
)


@pytest.mark.skims_test_group("unittesting")
def test_model_core_model_manifest() -> None:
    path: str = "skims/manifests/findings.json"
    expected: str = (
        json.dumps(
            sorted(finding.name for finding in core_model.FindingEnum),
            indent=2,
        )
        + "\n"
    )

    if SHOULD_UPDATE_TESTS:
        with open(path, "w") as handle_w:
            handle_w.write(expected)

    with open(path) as handle_r:
        assert handle_r.read() == expected


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


@pytest.mark.skims_test_group("unittesting")
def test_different_findings_name() -> None:
    threshold: float = 0.90
    for locale in core_model.LocalesEnum:
        for title_a, title_b in combinations(_get_findings_title(locale), 2):
            assert similar_ratio(title_a, title_b) < threshold
