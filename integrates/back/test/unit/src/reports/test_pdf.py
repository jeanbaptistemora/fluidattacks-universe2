from decimal import (
    Decimal,
)
import pytest
from reports.pdf import (
    get_severity,
)


@pytest.mark.parametrize(
    ["metric", "metric_value", "expected_result"],
    [
        ["access_vector", "0.395", "Local"],
        ["attack_vector", "0.62", "Red adyacente"],
        ["confidentiality_impact", "0.66", "Completo"],
        ["integrity_impact", "0.0", "Ninguno"],
        ["availability_impact", "0.275", "Parcial"],
        ["authentication", "0.704", "Ninguna"],
        ["exploitability", "1.0", "Alta"],
        ["confidence_level", "0.9", "No confirmado"],
        ["resolution_level", "0.9", "Temporal"],
        ["access_complexity", "0.71", "Bajo"],
    ],
)
def test_get_severity(
    metric: str,
    metric_value: str,
    expected_result: str,
) -> None:
    result = get_severity(metric, Decimal(metric_value))
    assert result == expected_result
