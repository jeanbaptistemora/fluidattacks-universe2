# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from gemfileparser import (
    Dependency,
    GemfileParser,
)
from typing import (
    Dict,
)


def parse_line(in_line: str, gem_file: str) -> Dict[str, str]:
    separator = "," if gem_file == "Gemfile" else " "
    line = in_line.split(separator)
    column_list = []
    for column in line:
        stripped_column = (
            column.replace("'", "")
            .replace('"', "")
            .replace("%q<", "")
            .replace("(", "")
            .replace(")", "")
            .replace("[", "")
            .replace("]", "")
            .strip()
        )
        if stripped_column.startswith("github: "):
            continue
        column_list.append(stripped_column)

    dep = Dependency()
    for column in column_list:
        for criteria, criteria_regex in GemfileParser.gemfile_regexes.items():
            match = criteria_regex.match(column)
            if match:
                setattr(dep, criteria, match.group(criteria))
                break
    return dep.to_dict()
