from aioextensions import (
    run,
)
from charts.generators.text_box.utils_vulnerabilities_remediation import (
    generate_all,
)

if __name__ == "__main__":
    run(generate_all("created"))
