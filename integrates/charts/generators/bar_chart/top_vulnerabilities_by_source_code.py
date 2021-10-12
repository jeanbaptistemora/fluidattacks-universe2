from aioextensions import (
    run,
)
from charts.generators.bar_chart.utils_top_vulnerabilities_by_source import (
    generate_all,
)

if __name__ == "__main__":
    run(generate_all(source="lines"))
