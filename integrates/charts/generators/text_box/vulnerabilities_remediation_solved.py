# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    run,
)
from charts.generators.text_box.utils_vulnerabilities_remediation import (
    generate_all,
)

if __name__ == "__main__":
    run(generate_all("solved", "Sprint exposure decrement"))
