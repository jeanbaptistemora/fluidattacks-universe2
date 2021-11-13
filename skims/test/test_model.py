import json
from model import (
    core_model,
)
import os
import pytest
from typing import (
    List,
)
from zone import (
    t,
)


@pytest.mark.skims_test_group("unittesting")
def test_model_core_model_manifest_findings() -> None:
    path: str = "skims/manifests/findings.json"
    expected: str = (
        json.dumps(
            {
                finding.name: {
                    locale.name: dict(
                        title=t(finding.value.title, locale=locale),
                    )
                    for locale in core_model.LocalesEnum
                }
                for finding in core_model.FindingEnum
                if finding.value.execution_queue
                != core_model.ExecutionQueue.none
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    expected_path = os.path.join(os.environ["STATE"], path)
    os.makedirs(os.path.dirname(expected_path), exist_ok=True)
    with open(expected_path, "w", encoding="utf-8") as handle_w:
        handle_w.write(expected)

    with open(path, encoding="utf-8") as handle_r:
        assert handle_r.read() == expected


@pytest.mark.skims_test_group("unittesting")
def test_model_core_model_manifest_queues() -> None:
    path: str = "skims/manifests/queues.json"
    expected: str = (
        json.dumps(
            {
                f"skims_{queue.name}": dict(
                    availability=queue.value.availability.value,
                    findings=sorted(
                        finding.name
                        for finding in core_model.FindingEnum
                        if finding.value.execution_queue == queue
                    ),
                )
                for queue in core_model.ExecutionQueue
                if queue != core_model.ExecutionQueue.none
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    expected_path = os.path.join(os.environ["STATE"], path)
    os.makedirs(os.path.dirname(expected_path), exist_ok=True)
    with open(expected_path, "w", encoding="utf-8") as handle_w:
        handle_w.write(expected)

    with open(path, encoding="utf-8") as handle_r:
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
