from aioextensions import (
    run,
)
from charts.generators.bar_chart.utils_top_vulnerabilities_by_source import (
    generate_all,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityType,
)

if __name__ == "__main__":
    run(generate_all(source=VulnerabilityType.INPUTS))
