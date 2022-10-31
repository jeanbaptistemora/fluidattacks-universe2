# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0


from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
import re
from typing import (
    Iterator,
    List,
    Pattern,
    Set,
    Tuple,
)


def check_digest(line: str) -> bool:
    digest_re: Pattern = re.compile(".*@sha256:[a-fA-F0-9]{64}")
    return bool(digest_re.search(line))


def get_joint_line(line_no: int, lines: list) -> str:
    joint_line: str = lines[line_no - 1].strip()[:-1] + " "
    for line in lines[line_no:]:
        joint_line += line[:-1] + " "
        if line.strip()[-1] != "\\":
            break
    return joint_line


def image_has_digest(content: str, path: str) -> Vulnerabilities:  # NOSONAR
    def iterator(vuln_lines: Set) -> Iterator[Tuple[int, int]]:
        for vuln_line in vuln_lines:
            yield vuln_line, 0

    commands_to_check = {"docker run", "podman run"}
    line_breaks: Set = set()
    vulns_found: Set = set()

    lines: List = content.splitlines()

    for line_number, line in enumerate(lines, start=1):
        if not line.lstrip().startswith("#") and any(
            command in line for command in commands_to_check
        ):
            if valid_line := line.split(" #")[0]:
                if valid_line.rstrip().endswith("\\"):
                    line_breaks.add(line_number)
                elif not check_digest(line):
                    vulns_found.add(line_number)

    for line_no in line_breaks:
        complete_line: str = get_joint_line(line_no, lines)
        if not check_digest(complete_line):
            vulns_found.add(line_no)

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f380.bash_image_has_digest",
        iterator=iterator(vulns_found),
        path=path,
        method=MethodsEnum.BASH_IMAGE_HAS_DIGEST,
    )
