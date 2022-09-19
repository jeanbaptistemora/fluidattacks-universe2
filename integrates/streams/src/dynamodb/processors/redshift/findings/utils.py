# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from typing import (
    Any,
)


def format_row_metadata(
    item: dict[str, Any],
) -> dict[str, Any]:
    return dict(
        id=item["id"],
        cvss_version=item["cvss_version"],
        group_name=item["group_name"],
        hacker_email=item["analyst_email"],
        requirements=item["requirements"],
        sorts=item["sorts"],
        title=item["title"],
    )
